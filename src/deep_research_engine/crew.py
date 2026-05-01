import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	EXASearchTool,
	ScrapeWebsiteTool,
	ArxivPaperTool,
	FileWriterTool
)

@CrewBase
class DeepResearchEngineCrew:
    """DeepResearchEngine crew"""

    @agent
    def senior_research_strategist(self) -> Agent:
        llm_config = self.agents_config["senior_research_strategist"].get("llm_config", {})
        llm_params = {
            "model": self.agents_config["senior_research_strategist"].get("llm", "groq/llama-3.3-70b-versatile"),
            "temperature": llm_config.get("temperature", 0.7),
            "max_tokens": llm_config.get("max_tokens", 8192),
        }
        if llm_config.get("top_p") is not None:
            llm_params["top_p"] = llm_config.get("top_p")
        if llm_config.get("top_k") is not None:
            llm_params["top_k"] = llm_config.get("top_k")
        
        fallback_model = self.agents_config["senior_research_strategist"].get("fallback_llm")
        if fallback_model:
            llm_params["fallbacks"] = [fallback_model]

        return Agent(
            config=self.agents_config["senior_research_strategist"],
            tools=[
                SerperDevTool(),
                EXASearchTool(),
                ScrapeWebsiteTool(),
                FileWriterTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(**llm_params),
        )
        
    
    @agent
    def other_steve_deep_research_mode(self) -> Agent:
        llm_config = self.agents_config["other_steve_deep_research_mode"].get("llm_config", {})
        llm_params = {
            "model": self.agents_config["other_steve_deep_research_mode"].get("llm", "openai/gpt-4o-mini"),
            "temperature": llm_config.get("temperature", 0.7),
            "max_tokens": llm_config.get("max_tokens", 8192),
        }
        if llm_config.get("top_p") is not None:
            llm_params["top_p"] = llm_config.get("top_p")
        if llm_config.get("top_k") is not None:
            llm_params["top_k"] = llm_config.get("top_k")

        fallback_model = self.agents_config["other_steve_deep_research_mode"].get("fallback_llm")
        if fallback_model:
            llm_params["fallbacks"] = [fallback_model]

        return Agent(
            config=self.agents_config["other_steve_deep_research_mode"],
            tools=[                SerperDevTool(),
                EXASearchTool(),
                ScrapeWebsiteTool(),
                ArxivPaperTool(),
                FileWriterTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(**llm_params),
        )
        
    
    @agent
    def other_steve_sift_fact_checker(self) -> Agent:
        llm_config = self.agents_config["other_steve_sift_fact_checker"].get("llm_config", {})
        llm_params = {
            "model": self.agents_config["other_steve_sift_fact_checker"].get("llm", "openai/gpt-4o-mini"),
            "temperature": llm_config.get("temperature", 0.7),
            "max_tokens": llm_config.get("max_tokens", 8192),
        }
        if llm_config.get("top_p") is not None:
            llm_params["top_p"] = llm_config.get("top_p")
        if llm_config.get("top_k") is not None:
            llm_params["top_k"] = llm_config.get("top_k")

        fallback_model = self.agents_config["other_steve_sift_fact_checker"].get("fallback_llm")
        if fallback_model:
            llm_params["fallbacks"] = [fallback_model]

        return Agent(
            config=self.agents_config["other_steve_sift_fact_checker"],
            tools=[                SerperDevTool(),
                EXASearchTool(),
                ScrapeWebsiteTool(),
                FileWriterTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(**llm_params),
        )
        
    
    @agent
    def other_steve_pragmatic_editor(self) -> Agent:
        llm_config = self.agents_config["other_steve_pragmatic_editor"].get("llm_config", {})
        llm_params = {
            "model": self.agents_config["other_steve_pragmatic_editor"].get("llm", "openai/mistralai/mistral-large"),
            "temperature": llm_config.get("temperature", 0.7),
            "max_tokens": llm_config.get("max_tokens", 8192),
        }
        if llm_config.get("top_p") is not None:
            llm_params["top_p"] = llm_config.get("top_p")
        if llm_config.get("top_k") is not None:
            llm_params["top_k"] = llm_config.get("top_k")

        fallback_model = self.agents_config["other_steve_pragmatic_editor"].get("fallback_llm")
        if fallback_model:
            llm_params["fallbacks"] = [fallback_model]

        return Agent(
            config=self.agents_config["other_steve_pragmatic_editor"],
            tools=[FileWriterTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(**llm_params),
        )
        
    
    @agent
    def other_steve_tree_of_thoughts_evaluator(self) -> Agent:
        llm_config = self.agents_config["other_steve_tree_of_thoughts_evaluator"].get("llm_config", {})
        llm_params = {
            "model": self.agents_config["other_steve_tree_of_thoughts_evaluator"].get("llm", "openrouter/z-ai/glm-4.7"),
            "temperature": llm_config.get("temperature", 0.7),
            "max_tokens": llm_config.get("max_tokens", 8192),
        }
        if llm_config.get("top_p") is not None:
            llm_params["top_p"] = llm_config.get("top_p")
        if llm_config.get("top_k") is not None:
            llm_params["top_k"] = llm_config.get("top_k")

        fallback_model = self.agents_config["other_steve_tree_of_thoughts_evaluator"].get("fallback_llm")
        if fallback_model:
            llm_params["fallbacks"] = [fallback_model]

        return Agent(
            config=self.agents_config["other_steve_tree_of_thoughts_evaluator"],
            tools=[FileWriterTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(**llm_params),
        )
        
    

    
    @task
    def strategy_formulation(self) -> Task:
        return Task(
            config=self.tasks_config["strategy_formulation"],
            markdown=False,
            
            
        )
    
    @task
    def deep_technical_research_execution(self) -> Task:
        return Task(
            config=self.tasks_config["deep_technical_research_execution"],
            markdown=False,
            
            
        )
    
    @task
    def sift_fact_checking_and_verification(self) -> Task:
        return Task(
            config=self.tasks_config["sift_fact_checking_and_verification"],
            markdown=False,
            
            
        )
    
    @task
    def research_methodology_evaluation(self) -> Task:
        return Task(
            config=self.tasks_config["research_methodology_evaluation"],
            markdown=False,
            
            
        )
    
    @task
    def technical_content_synthesis(self) -> Task:
        return Task(
            config=self.tasks_config["technical_content_synthesis"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the DeepResearchEngine crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            checkpoint=True,
            chat_llm="google/gemini-1.5-flash",
        )


