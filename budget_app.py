class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        # Título centrado en 30 caracteres con asteriscos
        title = f"{self.name:*^30}\n"
        
        items = ""
        for entry in self.ledger:
            desc = entry["description"][:23].ljust(23)
            amt = f"{entry['amount']:.2f}".rjust(7)
            items += f"{desc}{amt}\n"
            
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    title = "Percentage spent by category\n"
    
    # Calcular retiros por categoría y total general
    spent_per_category = []
    for cat in categories:
        spent = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_per_category.append(spent)
        
    total_spent = sum(spent_per_category)
    
    # Porcentajes redondeados a la decena hacia abajo
    percentages = []
    for spent in spent_per_category:
        if total_spent > 0:
            pct = int((spent / total_spent) * 100)
            percentages.append((pct // 10) * 10)
        else:
            percentages.append(0)

    # Construir barras de 100% a 0%
    chart = ""
    for i in range(100, -1, -10):
        chart += f"{str(i).rjust(3)}|"
        for pct in percentages:
            if pct >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"  

    " Línea horizontal separadora" 
    dashes = "    " + "-" * (len(categories) * 3 + 1) + "\n"
    
    "Nombres de categorías verticales" 

    names = [cat.name for cat in categories]
    max_len = max(len(name) for name in names)
    
    vertical_names = ""
    for i in range(max_len):
        vertical_names += "    "
        for name in names:
            if i < len(name):
                vertical_names += f" {name[i]} "
            else:
                vertical_names += "   "
        vertical_names += " "
        if i < max_len - 1:
            vertical_names += "\n"

    return title + chart + dashes + vertical_names
