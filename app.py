import streamlit as st
import random
import uuid
import datetime

class BudgetItem:
    def __init__(self, name, amount=0):
        self._name = name
        self._id = str(uuid.uuid4())
        self._amount = amount
        self._date = datetime.date.today()

    def details(self):
        raise NotImplementedError("Subclasses must implement details")

class Expense(BudgetItem):
    def __init__(self, name, amount, category):
        super().__init__(name, amount)
        self._category = category
        self._is_paid = False

    def mark_paid(self):
        self._is_paid = True
        return f"{self._name} marked as paid!"

    def details(self):
        status = "Paid" if self._is_paid else "Unpaid"
        return f"Expense: {self._name} | Amount: PKR {self._amount} | Category: {self._category} | Status: {status} | Date: {self._date}"

class Task(BudgetItem):
    def __init__(self, name, priority):
        super().__init__(name)
        self._priority = priority
        self._is_completed = False

    def mark_completed(self):
        self._is_completed = True
        return f"{self._name} marked as completed!"

    def details(self):
        status = "Completed" if self._is_completed else "Pending"
        return f"Task: {self._name} | Priority: {self._priority} | Status: {status} | Date: {self._date}"

class Household:
    def __init__(self, name):
        self._name = name
        self._budget = 0
        self._expenses = []
        self._tasks = []
        self._grocery_list = []
        self._household_id = str(uuid.uuid4())

    def set_budget(self, amount):
        self._budget = amount
        return f"Budget set to PKR {self._budget}"

    def add_expense(self, expense):
        self._expenses.append(expense)
        return f"Added expense: {expense._name}"

    def add_task(self, task):
        self._tasks.append(task)
        return f"Added task: {task._name}"

    def add_grocery_item(self, item):
        self._grocery_list.append(item)
        return f"Added to grocery list: {item}"

    def remove_grocery_item(self, item):
        if item in self._grocery_list:
            self._grocery_list.remove(item)
            return f"Removed from grocery list: {item}"
        return f"{item} not found in grocery list!"

    def get_suggestions(self, is_premium=False):
        total_expenses = sum(expense._amount for expense in self._expenses if not expense._is_paid)
        suggestions = []
        if total_expenses > self._budget * 0.8:
            suggestions.append("Warning: You're close to exceeding your budget! Reduce non-essential expenses.")
        if any(expense._category == "Grocery" for expense in self._expenses):
            suggestions.append("Buy groceries in bulk to save money.")
        if is_premium:
            suggestions.append(f"Premium Tip: Shop at [Local Store] this week for 5% off on groceries.")
            suggestions.append("Premium Report: Export your monthly expenses for better planning.")
        return suggestions if suggestions else ["All good! Keep managing your budget wisely."]

    def get_status(self):
        total_expenses = sum(expense._amount for expense in self._expenses)
        status = [f"Household: {self._name} | Budget: PKR {self._budget} | Total Expenses: PKR {total_expenses}"]
        status.append("Expenses:")
        status.extend([expense.details() for expense in self._expenses])
        status.append("Tasks:")
        status.extend([task.details() for task in self._tasks])
        status.append(f"Grocery List: {', '.join(self._grocery_list) if self._grocery_list else 'Empty'}")
        return status

def main():
    st.title(" Manage Your Household 🏡")
    st.write("Track expenses, manage tasks, and plan groceries with smart suggestions!")

    st.sidebar.title("مینو")
    menu_options = ["گھرانہ بنائیں", "بجٹ سیٹ کریں", "خرچہ شامل کریں", "خرچوں کا انتظام", "کام شامل کریں", "کاموں کا انتظام", "گروسری لسٹ", "سمارٹ مشورے", "گھرانے کی حالت"]
    selected_option = st.sidebar.selectbox("نیویگیشن", menu_options)

    if "household" not in st.session_state:
        st.session_state.household = None
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "is_premium" not in st.session_state:
        st.session_state.is_premium = False

    household = st.session_state.household

    if selected_option == "گھرانہ بنائیں":
        st.subheader("گھرانہ بنائیں یا منتخب کریں")
        household_name = st.text_input("گھرانے کا نام")
        if st.button("گھرانہ بنائیں"):
            if household_name:
                st.session_state.household = Household(household_name)
                st.session_state.message = f"گھرانہ بنایا گیا: {household_name}"
            else:
                st.session_state.message = "براہ کرم گھرانے کا نام درج کریں!"

    elif selected_option == "بجٹ سیٹ کریں" and household:
        st.subheader("ماہانہ بجٹ سیٹ کریں")
        budget_amount = st.number_input("بجٹ (PKR)", min_value=0, step=1000)
        if st.button("بجٹ سیٹ کریں"):
            st.session_state.message = household.set_budget(budget_amount)

    elif selected_option == "خرچہ شامل کریں" and household:
        st.subheader("خرچہ شامل کریں")
        col1, col2, col3 = st.columns(3)
        with col1:
            expense_name = st.text_input("خرچے کا نام")
        with col2:
            amount = st.number_input("رقم (PKR)", min_value=0, step=100)
        with col3:
            category = st.selectbox("زمرہ", ["گروسری", "یوٹیلیٹی", "دیگر"])
        if st.button("خرچہ شامل کریں"):
            if expense_name and amount:
                expense = Expense(expense_name, amount, category)
                st.session_state.message = household.add_expense(expense)
            else:
                st.session_state.message = "براہ کرم خرچے کا نام اور رقم درج کریں!"

    elif selected_option == "خرچوں کا انتظام" and household:
        st.subheader("خرچے کو ادا شدہ نشان زد کریں")
        expense_options = [expense._name for expense in household._expenses if not expense._is_paid]
        selected_expense = st.selectbox("خرچہ منتخب کریں", expense_options if expense_options else ["کوئی نہیں"])
        if st.button("ادا شدہ نشان زد کریں"):
            if selected_expense != "کوئی نہیں":
                expense = next((e for e in household._expenses if e._name == selected_expense), None)
                if expense:
                    st.session_state.message = expense.mark_paid()
            else:
                st.session_state.message = "کوئی غیر ادا شدہ خرچہ نہیں!"

    elif selected_option == "کام شامل کریں" and household:
        st.subheader("کام شامل کریں")
        col1, col2 = st.columns(2)
        with col1:
            task_name = st.text_input("کام کا نام")
        with col2:
            priority = st.selectbox("ترجیح", ["زیادہ", "درمیانی", "کم"])
        if st.button("کام شامل کریں"):
            if task_name:
                task = Task(task_name, priority)
                st.session_state.message = household.add_task(task)
            else:
                st.session_state.message = "براہ کرم کام کا نام درج کریں!"

    elif selected_option == "کاموں کا انتظام" and household:
        st.subheader("کام کو مکمل نشان زد کریں")
        task_options = [task._name for task in household._tasks if not task._is_completed]
        selected_task = st.selectbox("کام منتخب کریں", task_options if task_options else ["کوئی نہیں"])
        if st.button("مکمل نشان زد کریں"):
            if selected_task != "کوئی نہیں":
                task = next((t for t in household._tasks if t._name == selected_task), None)
                if task:
                    st.session_state.message = task.mark_completed()
            else:
                st.session_state.message = "کوئی زیر التوا کام نہیں!"

    elif selected_option == "گروسری لسٹ" and household:
        st.subheader("گروسری لسٹ کا انتظام")
        grocery_item = st.text_input("گروسری آئٹم")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("آئٹم شامل کریں"):
                if grocery_item:
                    st.session_state.message = household.add_grocery_item(grocery_item)
                else:
                    st.session_state.message = "براہ کرم گروسری آئٹم درج کریں!"
        with col2:
            if st.button("آئٹم ہٹائیں"):
                if grocery_item:
                    st.session_state.message = household.remove_grocery_item(grocery_item)
                else:
                    st.session_state.message = "براہ کرم گروسری آئٹم درج کریں!"

    elif selected_option == "سمارٹ مشورے" and household:
        st.subheader("سمارٹ مشورے")
        if st.button("مشورے حاصل کریں"):
            suggestions = household.get_suggestions(st.session_state.is_premium)
            st.session_state.message = "مشورے: " + "; ".join(suggestions)

    elif selected_option == "گھرانے کی حالت" and household:
        st.subheader("گھرانے کی حالت")
        for status in household.get_status():
            st.write(status)

    if st.session_state.message:
        st.info(st.session_state.message)

if __name__ == "__main__":
    main()
