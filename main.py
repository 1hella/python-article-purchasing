from fpdf import FPDF
import pandas as pd

df = pd.read_csv('articles.csv', dtype={'id': str})


class Article:
    def __init__(self, article_id):
        self.article_id = article_id
        self.name = df.loc[df['id'] == self.article_id, 'name'].squeeze()
        self.price = df.loc[df['id'] == self.article_id, 'price'].squeeze()

    def order(self):
        df.loc[df['id'] == self.article_id, 'in stock'] -= 1
        df.to_csv('articles.csv', index=False)

    def available(self):
        in_stock = df.loc[df['id'] == self.article_id, 'in stock'].squeeze()
        return in_stock > 0

    def get_id(self):
        return self.article_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price


class Receipt:
    def __init__(self, article):
        self.article = article

    def generate_pdf(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{self.article.get_id()}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article.get_name()}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.article.get_price()}", ln=1)

        pdf.output("receipt.pdf")


print(df)
article_id = input("Choose an article to buy: ")
article = Article(article_id)
if article.available():
    article.order()
    receipt = Receipt(article)
    receipt.generate_pdf()
