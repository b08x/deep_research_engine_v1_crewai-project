#!/usr/bin/env python
import sys
import os
import glob
from crewai import CheckpointConfig
from deep_research_engine.crew import DeepResearchEngineCrew
from deep_research_engine.utils import load_yaml_config

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = load_yaml_config("inputs.yaml")
    
    from_checkpoint = None
    if "--resume" in sys.argv:
        checkpoint_dir = ".checkpoints"
        if os.path.exists(checkpoint_dir):
            checkpoints = glob.glob(os.path.join(checkpoint_dir, "*.json"))
            if checkpoints:
                latest_checkpoint = max(checkpoints, key=os.path.getctime)
                print(f"Resuming from checkpoint: {latest_checkpoint}")
                from_checkpoint = CheckpointConfig(restore_from=latest_checkpoint)
            else:
                print("No checkpoints found in .checkpoints/")
        else:
            print("Checkpoint directory .checkpoints/ not found.")

    DeepResearchEngineCrew().crew().kickoff(inputs=inputs, from_checkpoint=from_checkpoint)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = load_yaml_config("inputs.yaml")
    try:
        DeepResearchEngineCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DeepResearchEngineCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = load_yaml_config("inputs.yaml")
    try:
        DeepResearchEngineCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
