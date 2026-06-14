from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama


# ---------------- TOOLS ----------------

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:   
    """Calculate attendance percentage and exam eligibility status.
    Takes total number of classes and number of classes attended."""
    
    percentage = (attended_classes / total_classes) * 100
    eligibility = "Eligible for Exam" if percentage >= 75 else "Not Eligible for Exam"
    return f"Attendance Percentage: {percentage:.2f}%, Status: {eligibility}"


@tool
def result_calculator(subject1: float, subject2: float, subject3: float,
                       subject4: float, subject5: float) -> str:   
    """Calculate average marks, grade and pass/fail status from marks of 5 subjects."""
    
    marks = [subject1, subject2, subject3, subject4, subject5]
    avg = sum(marks) / 5

    if avg >= 90:
        grade = "A"
    elif avg >= 75:
        grade = "B"
    elif avg >= 60:
        grade = "C"
    else:
        grade = "D"

    status = "Pass" if avg >= 50 else "Fail"
    return f"Average Marks: {avg:.2f}, Grade: {grade}, Status: {status}"


@tool
def fee_balance_calculator(total_fee: float, amount_paid: float) -> str:
    """Calculate the pending/remaining fee amount given a total amount due and 
    amount already paid. Use this whenever the user asks how much money is 
    still owed or left to pay, for ANY type of fee (course fee, hostel fee, 
    or any other fee), as long as both a total amount and a paid amount are given."""
    pending = total_fee - amount_paid
    return f"Pending Fee Amount: Rs.{pending:.2f}"


@tool
def library_fine_calculator(delayed_days: int) -> str:   
    """Calculate library fine amount. Fine is Rs.5 per delayed day."""
    
    fine = 5 * delayed_days
    return f"Library Fine Amount: Rs.{fine}"


@tool
def hostel_fee_calculator(monthly_fee: float, months_stayed: int) -> str:
    """Calculate TOTAL hostel fee by multiplying monthly hostel fee by number 
    of months stayed. Use ONLY when the user gives a monthly rate and a 
    number of months, and wants the total cost — NOT for 'how much is left to pay'."""
    total = monthly_fee * months_stayed
    return f"Total Hostel Fee: Rs.{total}"


# Bonus tool
students_db = {
    "S101": {"name": "Naruto Uzumaki", "course": "BECE", "year": 3},
    "S102": {"name": "Son Goku", "course": "BCSE", "year": 2},
    "S103": {"name": "Monkey D.Luffy", "course": "BME", "year": 4},
}

@tool
def student_info_tool(student_id: str) -> str:
    """Retrieve student details (name, course, year) using their Student ID."""
    
    student = students_db.get(student_id.upper())
    if student:
        return f"Name: {student['name']}, Course: {student['course']}, Year: {student['year']}"
    return "Student not found."


# ---------------- LLM ----------------
llm = ChatOllama(model="llama3.2", temperature=0)

# ---------------- PROMPT ----------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Smart College Assistant. Use the available tools to "
                "accurately answer student queries. Identify which tool(s) are "
                "needed for each query and call them with the correct inputs "
                "extracted from the user's message. If multiple values are needed, "
                "call multiple tools. "
                "IMPORTANT RULES: "
                "1. When stating your final answer, directly use the exact "
                "status/result returned by the tool without re-deriving it. "
                "2. Never add extra information not returned by a tool — do not "
                "expand abbreviations or guess full forms. "
                "3. For any 'how much is left/pending/owed to pay' question with "
                "a total and an amount paid, ALWAYS use fee_balance_calculator, "
                "regardless of whether it's about hostel, course, or any other fee."
                "4. Tool outputs contain ALL the information needed to answer — always "
                "report every field returned by the tool (e.g., name, course, AND year) "
                "in your final answer. Never claim information is unavailable if it was "
                "returned by a tool."),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# ---------------- AGENT ----------------
tools = [
    attendance_calculator,
    result_calculator,
    fee_balance_calculator,
    library_fine_calculator,
    hostel_fee_calculator,
    student_info_tool,
]

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# ---------------- TEST CASES ----------------
queries = [
    "I attended 72 classes out of 90. Am I eligible for exams?",
    "My marks are 95, 90, 88, 91 and 87. What is my grade?",
    "My course fee is 50000 and I have paid 35000. How much fee is pending?",
    "I returned a library book 8 days late. What is the fine amount?",
    "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
    "I attended 80 classes out of 100. My marks are 90, 85, 88, 92 and 95. "
    "My course fee is 60000 and I paid 45000. Provide: 1. Attendance Status 2. Grade 3. Pending Fee",
]

if __name__ == "__main__":
    # Run all required test cases
    for q in queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {q}")
        print("=" * 80)
        result = agent_executor.invoke({"input": q})
        print("\nFINAL ANSWER:", result["output"])

    # Interactive mode
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE")
    print(f"Available Student IDs in database: {', '.join(students_db.keys())}")
    print("Type your query below (or 'exit' to quit)")
    print("=" * 80)

    while True:
        user_query = input("\nYou: ")
        if user_query.lower() == "exit":
            break
        result = agent_executor.invoke({"input": user_query})
        print("\nAssistant:", result["output"])
