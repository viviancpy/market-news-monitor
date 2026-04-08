import time
from crewai import Crew, Process
from crew import detector, analyst, create_tasks


def run_market_monitor():
    print("--- Starting AI Market Monitoring Cycle ---")

    # Create a fresh set of tasks for this cycle
    tasks = create_tasks()

    market_crew = Crew(
        agents=[detector, analyst],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = market_crew.kickoff()
    print(f"\nCycle Result:\n{result}")


if __name__ == "__main__":
    # Run every 5 minutes
    while True:
        run_market_monitor()
        print("Sleeping for 5 minutes...")
        time.sleep(300)