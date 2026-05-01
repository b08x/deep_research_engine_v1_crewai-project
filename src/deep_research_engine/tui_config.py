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
from .models_fetcher import get_models_by_provider, get_all_providers

class AgentEditor(Vertical):
    """A widget for editing an agent's profile."""
    
    def __init__(self, agent_id: str, agent_data: Dict, **kwargs):
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.agent_data = agent_data
        self.providers = ["openai", "anthropic", "google", "groq", "mistral"]
        
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
            else:
                model_select.prompt = "Select a model"
        else:
            model_select.disabled = True
            model_select.prompt = f"No models found for {provider}"

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
    
    Button#save-agent, Button#save-task {
        background: #008800;
        color: white;
    }
    
    Button#save-agent:hover, Button#save-task:hover {
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
        padding-left: 2;
    }
    
    #agent-goal, #agent-backstory, #task-desc, #task-output {
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
                
                with TabPane("Settings", id="settings-tab"):
                    yield Vertical(id="settings-pane")
        yield Footer()

    def on_mount(self) -> None:
        self.load_data()
        self.refresh_settings()

    def load_data(self) -> None:
        self.agents_config = load_yaml_config("agents.yaml")
        self.tasks_config = load_yaml_config("tasks.yaml")
        
        agent_list = self.query_one("#agent-list", ListView)
        agent_list.clear()
        for agent_id in self.agents_config:
            agent_list.append(ListItem(Label(agent_id), id=f"list-{agent_id}"))
            
        task_list = self.query_one("#task-list", ListView)
        task_list.clear()
        for task_id in self.tasks_config:
            task_list.append(ListItem(Label(task_id), id=f"list-{task_id}"))

    def refresh_settings(self) -> None:
        settings_pane = self.query_one("#settings-pane")
        settings_pane.remove_children()
        
        settings_pane.mount(Label("[bold cyan]API Key Status Check[/bold cyan]"))
        providers = ["OPENAI", "ANTHROPIC", "GEMINI", "GROQ", "MISTRAL"]
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
            self.agents_config[agent_id]["llm"] = f"{provider}/{model}"
        
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

    def action_save_all(self) -> None:
        save_yaml_config("agents.yaml", self.agents_config)
        save_yaml_config("tasks.yaml", self.tasks_config)
        self.notify("All configurations saved!")

def main():
    app = CrewConfigApp()
    app.run()

if __name__ == "__main__":
    main()
