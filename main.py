from typing import Annotated, Literal, TypedDict

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

from tools.system_tools import execute_terminal_command, manage_local_file

tools_registry = {
	"execute_terminal_command": execute_terminal_command,
	"manage_local_file": manage_local_file
}


class AgentState(TypedDict):
	messages: Annotated[list[BaseMessage], add_messages]


llm = ChatOllama(model="llama3.1", temperature=0.1)
llm_with_tools = llm.bind_tools(list(tools_registry.values()))


def call_model(state: AgentState):
	"""Submits state array logs into our local Llama brain module."""
	messages = state["messages"]

	if len(messages) == 1:
		# Added explicit Markdown reinforcement to force structured tool choices
		system_instructions = (
			"You are a highly capable local AI OS Agent. "
			"You have complete authorization to create/read files and execute shell terminal commands. "
			"When asked to perform a task like checking disk usage or making a file, you MUST call the "
			"appropriate tool immediately. Do not try to answer without using a tool if action is required."
		)
		messages = [HumanMessage(content=system_instructions)] + messages

	response = llm_with_tools.invoke(messages)
	return {"messages": [response]}


def execute_tools(state: AgentState):
	"""Parses tool invocations passed from the brain and executes actual python routines."""
	last_message = state["messages"][-1]
	tool_messages = []

	if hasattr(last_message, "tool_calls") and last_message.tool_calls:
		for call in last_message.tool_calls:
			tool_name = call["name"]
			tool_args = call["args"]

			if tool_name in tools_registry:
				tool_output = tools_registry[tool_name].invoke(tool_args)
				tool_messages.append(
					ToolMessage(content=str(tool_output), tool_call_id=call["id"])
				)
	return {"messages": tool_messages}


def router_edge(state: AgentState) -> Literal["execute_tools", "__end__"]:
	"""Decides if the state graph must loop to execute additional steps or terminate."""
	last_message = state["messages"][-1]
	if hasattr(last_message, "tool_calls") and last_message.tool_calls:
		return "execute_tools"
	return "__end__"


# Assemble the architectural graph structure cleanly
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("execute_tools", execute_tools)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", router_edge)
workflow.add_edge("execute_tools", "agent")

agent_app = workflow.compile()

if __name__ == "__main__":
	print("🚀 Powerful Local AI Agent Node Initialized. (Type 'exit' to quit)")
	while True:
		user_input = input("\nEnter Task Execution Goal: ")
		if user_input.lower() in ["exit", "quit"]:
			break

		initial_state = {"messages": [HumanMessage(content=user_input)]}

		for output in agent_app.stream(initial_state):
			for node, data in output.items():
				print(f"\n[SYSTEM NODE INVOCATION: {node.upper()}]")
				latest_msg = data["messages"][-1]
				if hasattr(latest_msg, "content") and latest_msg.content:
					print(latest_msg.content)
