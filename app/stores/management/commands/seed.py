import random
from datetime import date

from django.core.management.base import BaseCommand
from products.models import Product
from stores.models import Address, Stock, Store, StoreType
from users.models import Employee


class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs) -> None:
        """Seed database."""
        self.stdout.write("Seeding database...")
        self._create_products()
        self._create_ho()
        self._create_dealers()
        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))

    def _create_products(self) -> None:
        """Create products."""
        products = [
            ("Apple", "iPhone 15", 999.99, date(2023, 9, 22)),
            ("Apple", "iPhone 15 Pro", 1199.99, date(2023, 9, 22)),
            ("Samsung", "Galaxy S24", 899.99, date(2024, 1, 17)),
            ("Samsung", "Galaxy S24 Ultra", 1299.99, date(2024, 1, 17)),
            ("Sony", "WH-1000XM5", 349.99, date(2022, 5, 12)),
            ("Sony", "PlayStation 5", 499.99, date(2020, 11, 12)),
            ("Apple", "MacBook Pro 14", 1999.99, date(2023, 11, 7)),
            ("Samsung", "Galaxy Tab S9", 799.99, date(2023, 8, 11)),
            ("Sony", "WF-1000XM5", 279.99, date(2023, 7, 26)),
            ("Apple", "iPad Pro 12.9", 1099.99, date(2022, 3, 18)),
        ]
        self.products = []
        for brand, model, price, release_date in products:
            product, _ = Product.objects.get_or_create(
                brand=brand,
                model=model,
                defaults={"price": price, "release_date": release_date},
            )
            self.products.append(product)
        self.stdout.write(f"Created {len(self.products)} products")

    def _create_ho(self) -> None:
        """Create head office with one employee."""
        address, _ = Address.objects.get_or_create(
            country="USA",
            city="New York",
            street="5th Avenue",
            house=1,
        )
        ho, _ = Store.objects.get_or_create(
            type=StoreType.HO,
            defaults={"name": "Head Office", "address": address},
        )
        employee, created = Employee.objects.get_or_create(
            username="ho_manager",
            defaults={
                "first_name": "John",
                "last_name": "Smith",
                "email": "ho_manager@electronics.com",
                "phone": "+1234567890",
                "store": ho,
                "is_staff": True,
            },
        )
        if created:
            employee.set_password("password123")
            employee.save()
        self.ho = ho
        self.stdout.write(f"Created HO: {ho.name}")

    def _create_dealers(self) -> None:
        """Create 10 dealers with employees and stock."""
        dealers_data = [
            ("Electronics Plus", "USA", "Los Angeles", "Sunset Blvd", 100),
            ("TechWorld", "USA", "Chicago", "Michigan Ave", 200),
            ("GadgetHub", "UK", "London", "Oxford Street", 10),
            ("TechStore Berlin", "Germany", "Berlin", "Unter den Linden", 5),
            ("ElectroShop", "France", "Paris", "Champs Elysees", 15),
            ("DigiZone", "Canada", "Toronto", "Yonge Street", 50),
            ("SmartTech", "Australia", "Sydney", "George Street", 25),
            ("FutureTech", "Japan", "Tokyo", "Shibuya", 1),
            ("TechCity", "UAE", "Dubai", "Sheikh Zayed Rd", 100),
            ("MegaElectro", "Netherlands", "Amsterdam", "Damrak", 30),
        ]
        for name, country, city, street, house in dealers_data:
            address, _ = Address.objects.get_or_create(
                country=country,
                city=city,
                street=street,
                house=house,
            )
            dealer, _ = Store.objects.get_or_create(
                name=name,
                defaults={
                    "type": StoreType.DEALER,
                    "address": address,
                    "daily_revenue": random.uniform(100, 10000),
                },
            )
            self._create_dealer_employees(dealer)
            self._create_dealer_stock(dealer)
            self.stdout.write(f"Created dealer: {dealer.name}")

    def _create_dealer_employees(self, dealer: Store) -> None:
        """Create at least 2 employees for dealer."""
        employees_data = [
            (f"{dealer.name.lower().replace(' ', '_')}_manager", "Manager"),
            (f"{dealer.name.lower().replace(' ', '_')}_staff", "Staff"),
        ]
        for username, role in employees_data:
            employee, created = Employee.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": role,
                    "last_name": dealer.name,
                    "email": f"{username}@electronics.com",
                    "phone": f"+{random.randint(10000000000, 19999999999)}",
                    "store": dealer,
                },
            )
            if created:
                employee.set_password("password123")
                employee.save()

    def _create_dealer_stock(self, dealer: Store) -> None:
        """Create stock for dealer."""
        for product in random.sample(
            self.products,
            random.randint(3, len(self.products)),
        ):
            Stock.objects.get_or_create(
                store=dealer,
                product=product,
                defaults={"quantity": random.randint(0, 50)},
            )
