from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from tools import MarketTools

# Initialize shared tools
search_tool = SerperDevTool()
sr_tool = MarketTools.query_starrocks
whatsapp_tool = MarketTools.send_whatsapp_msg

# Define Agents
detector = Agent(
    role='Volatility Scout',
    goal='Identify movements in BTC/EUR prices that exceed 2% in 5 minutes',
    backstory='An expert in real-time data monitoring within StarRocks. You focus only on the numbers.',
    tools=[sr_tool],
    verbose=True
)

analyst = Agent(
    role='Contextual Reporter',
    goal='Explain WHY a price move happened and notify the user if it is critical',
    backstory='A financial analyst who connects data spikes to real-world news using web search.',
    tools=[search_tool, whatsapp_tool],
    verbose=True
)


# Define Tasks
def create_tasks():
    t1 = Task(
        description="Query the 'v_crypto_prices_eur' view. Compare the latest price to the 5-minute average.",
        expected_output="A report stating the percentage change and current price.",
        agent=detector
    )

    t2 = Task(
        description=(
            "Search for news related to the price movement from Task 1. "
            "If movement is > 2%, send a WhatsApp alert that includes: "
            "1) the percentage change and current price, "
            "2) a 2-3 sentence news summary explaining WHY the price moved. "
            "The news summary MUST be included inside the WhatsApp message itself."
        ),
        expected_output="A confirmation that the WhatsApp alert was sent, including the full message text with news summary.",
        agent=analyst,
        context=[t1]
    )
    return [t1, t2]