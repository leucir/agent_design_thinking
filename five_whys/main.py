from five_whys_agent import FiveWhysAgent
from models import MODELS


# Usage example
def main():
    """Example usage of the 5 Whys agent"""
    
    # Initialize the agent
    agent = FiveWhysAgent(llm=MODELS["LMSTUDIO_PHI4"])
    
    # Define a problem
    problem = "Cancer is a disease that affects the body. Why is it so common?"
    
    # Run the analysis
    print("🔍 Starting 5 Whys Analysis...")
    print(f"Problem: {problem}")
    print("=" * 50)
    
    result = agent.analyze(problem, max_whys=5)
    
    # Display results
    print("\n📊 ANALYSIS RESULTS")
    print("=" * 50)
    
    print(f"\n🎯 Root Cause: {result['root_cause']}")
    
    print(f"\n🔗 Why Chain:")
    for i, why in enumerate(result['why_chain'], 1):
        print(f"  {i}. {why['question']}")
        print(f"     → {why['answer']}")
        if why.get('evidence'):
            print(f"     Evidence: {why['evidence']}")
        print()
    
    print(f"\n💡 Recommended Solutions:")
    for i, solution in enumerate(result['solutions'], 1):
        print(f"  {i}. {solution}")
    
    print(f"\n📋 Full Report:")
    print(result['report'])
    
    print(f"\n⏱️  Processing Time: {result['processing_time']:.2f} seconds")
    print(f"🏁 Stop Reason: {result['stop_reason']}")
    
    if result['errors']:
        print(f"\n⚠️  Errors: {result['errors']}")

if __name__ == "__main__":
    main()
