class Category:

    def __init__(self, budget_category):
        self.budget_category = budget_category
        self.ledger = []

    def __str__(self):
        title_line = f"{self.budget_category:*^30}\n"
        ledger_items = ''
        total = 0
        for item in self.ledger:
            ledger_items += f"{item['description'][0:23]:23}" + \
                f"{item['amount']:>7.2f}" + '\n'
            total += item['amount']
        budget_output = title_line + ledger_items + \
            'Total: ' + str(round(total, 2))
        return budget_output

    def deposit(self, amount, description=''):
        data = {'amount': amount, 'description': description}
        self.ledger.append(data)

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            data = {'amount': -amount, 'description': description}
            self.ledger.append(data)
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for amt in self.ledger:
            balance += amt['amount']
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, 'Transfer to ' + category.budget_category)
            category.deposit(amount, 'Transfer from ' + self.budget_category)
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True


def create_spend_chart(categories):
    withdrawals = []
    for category in categories:
        total = sum([amt['amount']
                    for amt in category.ledger if amt['amount'] < 0])
        withdrawals.append(total)
    percent_total = sum(withdrawals)
    percentages = [withdrawal / percent_total *
                   100 for withdrawal in withdrawals]

    budget_chart = 'Percentage spent by category\n'
    for i in range(100, -10, -10):
        budget_chart += str(i).rjust(3) + '| '
        for percentage in percentages:
            if percentage >= i:
                budget_chart += 'o  '
            else:
                budget_chart += '   '
        budget_chart += '\n'
    budget_chart += '    ' + '-' * (len(categories) * 3 + 1) + '\n'

    max_length = max(len(category.budget_category) for category in categories)

    for i in range(max_length):
        budget_chart += '     '
        for category in categories:
            if i < len(category.budget_category):
                budget_chart += category.budget_category[i] + '  '
            else:
                budget_chart += '   '
        if i != max_length - 1:
            budget_chart += '\n'
    return budget_chart
