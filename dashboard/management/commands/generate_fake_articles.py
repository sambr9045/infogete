# myapp/management/commands/generate_fake_articles.py
from django.core.management.base import BaseCommand
from faker import Faker
from dashboard.models import article
import random
import uuid

class Command(BaseCommand):
    help = 'Generate fake articles for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(200):  # Generate 10 fake articles
            title = fake.sentence()
            category = fake.word()
            content = fake.paragraphs(3)
            views = random.randint(100, 1000)
            likes = random.randint(50, 500)
            success_ratio = f"{random.uniform(0, 1) * 100:.2f}%"
            created_at = fake.date_time_this_decade()

            article.objects.create(
                article_title=title,
                category=category,
                content='\n'.join(content),
                views=views,
                likes=likes,
                success_ratio=success_ratio,
                created_at=created_at
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated fake articles'))
