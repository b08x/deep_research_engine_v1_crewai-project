import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Button,
    Header,
    Footer,
    Input,
    Label,
    ListItem,
    ListView,
    Select,
    Static,
    TabbedContent,
    TabPane,
    TextArea,
    Switch,
)
from textual.binding import Binding
from textual import on, work
from textual.screen import Screen
from textual.message import Message

from .utils import load_yaml_config, save_yaml_config, validate_api_key, get_env_var
from .models_fetcher import get_models_by_provider, get_all_providers, get_model_capabilities

class AgentEditor(Vertical):
    """A widget for editing an agent's profile."""
    
    def __init__(self, agent_id: str, agent_data: Dict, **kwargs):
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.agent_data = agent_data
        self.providers = ["openai", "anthropic", "google", "groq", "mistral", "openrouter"]
        capabilities = agent_data.get("requires_capabilities", {})
        self.capability_requirements = {
            "vision": capabilities.get("vision", False),
            "reasoning": capabilities.get("reasoning", False),
            "tool_calling": capabilities.get("tool_calling", False),
            "structured_output": capabilities.get("structured_output", False),
        }
        self.llm_config = self.agent_data.get("llm_config", {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": None,
            "max_tokens": 8192,
        })
        
    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield Label(f"Editing Agent: [bold cyan]{self.agent_id}[/bold cyan]")
            
            yield Label("Role")
            yield Input(value=str(self.agent_data.get("role", "")), id="agent-role")
            
            yield Label("Goal")
            yield TextArea(str(self.agent_data.get("goal", "")), id="agent-goal")
            
            yield Label("Backstory")
            yield TextArea(str(self.agent_data.get("backstory", "")), id="agent-backstory")
            
            yield Label("LLM Provider")
            current_model = self.agent_data.get("llm", "")
            current_provider = "openai" # Default
            if "/" in current_model:
                current_provider = current_model.split("/")[0]
            
            yield Select(
                [(p.capitalize(), p) for p in self.providers],
                value=current_provider,
                id="agent-provider"
            )
            
            yield Label("Model")
            yield Select([], id="agent-model", prompt="Select a model")
            yield Static("", id="cap-warning")
            
            yield Label("Capability Requirements")
            with Vertical(classes="cap-group"):
                with Horizontal():
                    yield Switch(value=self.capability_requirements["vision"], id="agent-cap-vision")
                    yield Label(" Vision Support", classes="cap-label")
                    yield Switch(value=self.capability_requirements["reasoning"], id="agent-cap-reasoning")
                    yield Label(" Reasoning Support", classes="cap-label")
                with Horizontal():
                    yield Switch(value=self.capability_requirements["tool_calling"], id="agent-cap-tool-calling")
                    yield Label(" Tool Calling", classes="cap-label")
                    yield Switch(value=self.capability_requirements["structured_output"], id="agent-cap-structured-output")
                    yield Label(" Structured Output", classes="cap-label")
            
            yield Label("LLM Configuration")
            with Horizontal(classes="llm-param-row"):
                with Vertical(classes="llm-param-col"):
                    yield Label("Temperature")
                    temp = self.llm_config.get("temperature")
                    yield Input(value=str(temp if temp is not None else 0.7), placeholder="0.7", type="number", id="agent-llm-temperature")
                with Vertical(classes="llm-param-col"):
                    yield Label("Top P")
                    tp = self.llm_config.get("top_p")
                    yield Input(value=str(tp if tp is not None else 0.9), placeholder="0.9", type="number", id="agent-llm-top-p")
            
            with Horizontal(classes="llm-param-row"):
                with Vertical(classes="llm-param-col"):
                    yield Label("Top K")
                    tk = self.llm_config.get("top_k")
                    yield Input(value=str(tk if tk is not None else ""), placeholder="None", type="number", id="agent-llm-top-k")
                with Vertical(classes="llm-param-col"):
                    yield Label("Max Tokens")
                    mt = self.llm_config.get("max_tokens")
                    yield Input(value=str(mt if mt is not None else 8192), placeholder="8192", type="number", id="agent-llm-max-tokens")
            
            with Horizontal(id="action-buttons"):
                yield Button("Save Changes", variant="success", id="save-agent")
                yield Button("Reset", variant="primary", id="reset-agent")

    def on_mount(self) -> None:
        self.update_models(self.query_one("#agent-provider", Select).value)

    @on(Select.Changed, "#agent-provider")
    def on_provider_changed(self, event: Select.Changed) -> None:
        self.update_models(event.value)

    @work
    async def update_models(self, provider: str) -> None:
        model_select = self.query_one("#agent-model", Select)
        cap_warning = self.query_one("#cap-warning", Static)
        
        # Reset warning when provider changes
        cap_warning.update("")
        
        if not validate_api_key(provider):
            model_select.disabled = True
            model_select.prompt = f"API Key missing for {provider}"
            return
        
        model_select.disabled = False
        model_select.prompt = "Fetching models..."
        
        models = get_models_by_provider(provider)
        if models:
            options = [(m, m) for m in models]
            model_select.set_options(options)
            
            # Try to set current model if it matches
            current_llm = self.agent_data.get("llm", "")
            if current_llm in models:
                model_select.value = current_llm
                self._check_capabilities(current_llm)
            else:
                model_select.prompt = "Select a model"
                cap_warning.update("")
        else:
            model_select.disabled = True
            model_select.prompt = f"No models found for {provider}"
            cap_warning.update("")

    def _check_capabilities(self, model: str) -> None:
        """Check model capabilities against agent requirements and update warning."""
        cap_warning = self.query_one("#cap-warning", Static)
        
        if not model:
            cap_warning.update("")
            return
        
        caps = get_model_capabilities(model)
        if not caps:
            cap_warning.update("")
            return
        
        warnings = []
        
        if self.capability_requirements.get("vision") and not caps.get("supports_vision"):
            warnings.append("[yellow]Model does not support vision[/yellow]")
        
        if self.capability_requirements.get("reasoning") and not caps.get("supports_reasoning"):
            warnings.append("[yellow]Model does not support reasoning[/yellow]")
        
        if self.capability_requirements.get("tool_calling") and not caps.get("supports_function_calling"):
            warnings.append("[yellow]Model does not support tool calling[/yellow]")
        
        if self.capability_requirements.get("structured_output") and not caps.get("supports_response_schema"):
            warnings.append("[yellow]Model does not support structured output[/yellow]")
        
        if warnings:
            cap_warning.update("[red]Capability Warning:[/red] " + " | ".join(warnings))
        else:
            cap_warning.update("[green]All capabilities satisfied[/green]")

    @on(Select.Changed, "#agent-model")
    def on_model_changed(self, event: Select.Changed) -> None:
        if event.value:
            self._check_capabilities(event.value)

class TaskEditor(Vertical):
    """A widget for editing a task's definition."""
    
    def __init__(self, task_id: str, task_data: Dict, agents: List[str], **kwargs):
        super().__init__(**kwargs)
        self.task_id = task_id
        self.task_data = task_data
        self.agents = agents
        
    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield Label(f"Editing Task: [bold magenta]{self.task_id}[/bold magenta]")
            
            yield Label("Description")
            yield TextArea(str(self.task_data.get("description", "")), id="task-desc")
            
            yield Label("Expected Output")
            yield TextArea(str(self.task_data.get("expected_output", "")), id="task-output")
            
            yield Label("Assigned Agent")
            yield Select(
                [(a, a) for a in self.agents],
                value=self.task_data.get("agent", ""),
                id="task-agent"
            )
            
            with Horizontal(id="action-buttons"):
                yield Button("Save Changes", variant="success", id="save-task")
                yield Button("Reset", variant="primary", id="reset-task")

class InputEditor(Vertical):
    """A widget for editing run input parameters."""
    
    def __init__(self, inputs_data: Dict, **kwargs):
        super().__init__(**kwargs)
        self.inputs_data = inputs_data
        
    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield Label("[bold cyan]Run Parameters[/bold cyan]")
            for key, value in self.inputs_data.items():
                yield Label(key.replace("_", " ").capitalize())
                yield TextArea(str(value), id=f"input-{key}", classes="input-textarea")
            
            with Horizontal(id="action-buttons"):
                yield Button("Save Parameters", variant="success", id="save-inputs")

class CrewConfigApp(App):
    """A Textual app to configure CrewAI agents and tasks."""
    
    CSS = """
    Screen {
        background: #0f0f1b;
    }
    
    Header {
        background: #2b2b45;
        color: #00ffff;
        text-style: bold;
    }
    
    #main-container {
        padding: 1;
    }
    
    TabbedContent {
        background: #1a1a2e;
        border: solid #00ffff 20%;
    }
    
    TabPane {
        padding: 1;
    }
    
    Label {
        margin-top: 1;
        color: #a0a0c0;
        text-style: bold;
    }
    
    Input, TextArea, Select {
        margin-bottom: 1;
        border: solid #3b3b5c;
        background: #0f0f1b;
        color: #e0e0e0;
    }
    
    Input:focus, TextArea:focus, Select:focus {
        border: double #00ffff;
        background: #1a1a2e;
    }
    
    #action-buttons {
        height: auto;
        margin-top: 2;
    }
    
    Button {
        margin-right: 2;
        border: none;
    }
    
    Button#save-agent, Button#save-task, Button#save-inputs {
        background: #008800;
        color: white;
    }
    
    Button#save-agent:hover, Button#save-task:hover, Button#save-inputs:hover {
        background: #00aa00;
    }
    
    ListView {
        width: 35;
        height: 100%;
        border-right: solid #3b3b5c;
        background: #16162a;
    }
    
    ListItem {
        padding: 1;
        color: #8080a0;
    }
    
    ListItem.selected {
        background: #00ffff 15%;
        color: #00ffff;
        text-style: bold;
        border-left: solid #00ffff;
    }
    
    .editor-pane {
        width: 1fr;
        height: 100%;
        padding-left: 2;
    }
    
    #agent-goal, #agent-backstory, #task-desc, #task-output, .input-textarea {
        height: 8;
    }
    
    .status-ok { color: #00ff00; }
    .status-err { color: #ff0000; }
    
    Static.api-status {
        padding: 1;
        margin: 1;
        background: #16162a;
        border: solid #3b3b5c;
    }

    .cap-group {
        height: auto;
        margin-bottom: 1;
        border: solid #3b3b5c 10%;
        padding: 1;
    }

    .llm-param-row {
        height: auto;
        margin-bottom: 1;
    }

    .llm-param-col {
        width: 1fr;
        margin-right: 2;
    }

    .cap-label {
        width: 1fr;
        margin-left: 1;
        margin-top: 1;
        color: #8080a0;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("ctrl+s", "save_all", "Save All", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main-container"):
            with TabbedContent():
                with TabPane("Agents", id="agents-tab"):
                    with Horizontal():
                        yield ListView(id="agent-list")
                        yield Vertical(id="agent-editor-container", classes="editor-pane")
                
                with TabPane("Tasks", id="tasks-tab"):
                    with Horizontal():
                        yield ListView(id="task-list")
                        yield Vertical(id="task-editor-container", classes="editor-pane")
                
                with TabPane("Run Parameters", id="inputs-tab"):
                    yield Vertical(id="inputs-editor-container")

                with TabPane("Settings", id="settings-tab"):
                    yield Vertical(id="settings-pane")
        yield Footer()

    def on_mount(self) -> None:
        self.load_data()
        self.refresh_settings()

    def load_data(self) -> None:
        self.agents_config = load_yaml_config("agents.yaml")
        self.tasks_config = load_yaml_config("tasks.yaml")
        self.inputs_config = load_yaml_config("inputs.yaml")
        
        agent_list = self.query_one("#agent-list", ListView)
        agent_list.clear()
        for agent_id in self.agents_config:
            agent_list.append(ListItem(Label(agent_id), id=f"list-{agent_id}"))
            
        task_list = self.query_one("#task-list", ListView)
        task_list.clear()
        for task_id in self.tasks_config:
            task_list.append(ListItem(Label(task_id), id=f"list-{task_id}"))

        inputs_container = self.query_one("#inputs-editor-container")
        inputs_container.remove_children()
        inputs_container.mount(InputEditor(self.inputs_config))

    def refresh_settings(self) -> None:
        settings_pane = self.query_one("#settings-pane")
        settings_pane.remove_children()
        
        settings_pane.mount(Label("[bold cyan]API Key Status Check[/bold cyan]"))
        providers = ["OPENAI", "ANTHROPIC", "GEMINI", "GROQ", "MISTRAL", "OPENROUTER"]
        for p in providers:
            key = f"{p}_API_KEY"
            val = get_env_var(key)
            status = "[bold green]VALID[/bold green]" if val else "[bold red]MISSING[/bold red]"
            settings_pane.mount(Static(f"{key}: {status}", classes="api-status"))

    @on(ListView.Selected, "#agent-list")
    def on_agent_selected(self, event: ListView.Selected) -> None:
        if not event.item: return
        agent_id = event.item.id.replace("list-", "") if event.item.id else ""
        if agent_id not in self.agents_config: return
        container = self.query_one("#agent-editor-container")
        container.remove_children()
        container.mount(AgentEditor(agent_id, self.agents_config[agent_id]))

    @on(ListView.Selected, "#task-list")
    def on_task_selected(self, event: ListView.Selected) -> None:
        if not event.item: return
        task_id = event.item.id.replace("list-", "") if event.item.id else ""
        if task_id not in self.tasks_config: return
        container = self.query_one("#task-editor-container")
        container.remove_children()
        container.mount(TaskEditor(task_id, self.tasks_config[task_id], list(self.agents_config.keys())))

    @on(Button.Pressed, "#save-agent")
    def on_save_agent(self, event: Button.Pressed) -> None:
        editor = self.query_one(AgentEditor)
        agent_id = editor.agent_id
        
        self.agents_config[agent_id]["role"] = self.query_one("#agent-role", Input).value
        self.agents_config[agent_id]["goal"] = self.query_one("#agent-goal", TextArea).text
        self.agents_config[agent_id]["backstory"] = self.query_one("#agent-backstory", TextArea).text
        
        provider = self.query_one("#agent-provider", Select).value
        model = self.query_one("#agent-model", Select).value
        if provider and model:
            if model.startswith(f"{provider}/"):
                self.agents_config[agent_id]["llm"] = model
            else:
                self.agents_config[agent_id]["llm"] = f"{provider}/{model}"
        
        self.agents_config[agent_id]["requires_capabilities"] = {
            "vision": self.query_one("#agent-cap-vision", Switch).value,
            "reasoning": self.query_one("#agent-cap-reasoning", Switch).value,
            "tool_calling": self.query_one("#agent-cap-tool-calling", Switch).value,
            "structured_output": self.query_one("#agent-cap-structured-output", Switch).value,
        }
        
        top_k_input = self.query_one("#agent-llm-top-k", Input).value
        top_k = top_k_input if top_k_input else None
        
        self.agents_config[agent_id]["llm_config"] = {
            "temperature": float(self.query_one("#agent-llm-temperature", Input).value),
            "top_p": float(self.query_one("#agent-llm-top-p", Input).value),
            "top_k": float(top_k) if top_k is not None else None,
            "max_tokens": int(self.query_one("#agent-llm-max-tokens", Input).value),
        }
        
        save_yaml_config("agents.yaml", self.agents_config)
        self.notify(f"Agent {agent_id} saved successfully!")

    @on(Button.Pressed, "#save-task")
    def on_save_task(self, event: Button.Pressed) -> None:
        editor = self.query_one(TaskEditor)
        task_id = editor.task_id
        
        self.tasks_config[task_id]["description"] = self.query_one("#task-desc", TextArea).text
        self.tasks_config[task_id]["expected_output"] = self.query_one("#task-output", TextArea).text
        self.tasks_config[task_id]["agent"] = self.query_one("#task-agent", Select).value
        
        save_yaml_config("tasks.yaml", self.tasks_config)
        self.notify(f"Task {task_id} saved successfully!")

    @on(Button.Pressed, "#save-inputs")
    def on_save_inputs(self, event: Button.Pressed) -> None:
        for key in self.inputs_config:
            self.inputs_config[key] = self.query_one(f"#input-{key}", TextArea).text
        
        save_yaml_config("inputs.yaml", self.inputs_config)
        self.notify("Run parameters saved successfully!")

    def action_save_all(self) -> None:
        save_yaml_config("agents.yaml", self.agents_config)
        save_yaml_config("tasks.yaml", self.tasks_config)
        save_yaml_config("inputs.yaml", self.inputs_config)
        self.notify("All configurations saved!")

def main():
    app = CrewConfigApp()
    app.run()

if __name__ == "__main__":
    main()
