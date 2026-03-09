from __future__ import annotations

import argparse
import random
import uuid
from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models.card import Card
from app.db.models.merchant import Merchant
from app.db.models.user import User
from app.db.session import SessionLocal
from app.domains.enums import CardBrand, CardStatus, MerchantCategory


@dataclass
class SeedConfig:
    seed: int
    users: int
    merchants: int
    cards_per_user: int
    reset: bool


def parse_args() -> SeedConfig:
    p = argparse.ArgumentParser(description="Seed base entities for Fraud project.")
    p.add_argument("--seed", type=int, default=123)
    p.add_argument("--users", type=int, default=20)
    p.add_argument("--merchants", type=int, default=40)
    p.add_argument("--cards-per-user", type=int, default=2)
    p.add_argument("--reset", action="store_true", help="TRUNCATE tables (dev only)")
    a = p.parse_args()

    return SeedConfig(
        seed=a.seed,
        users=a.users,
        merchants=a.merchants,
        cards_per_user=a.cards_per_user,
        reset=a.reset,
    )


def reset_db(session: Session) -> None:
    """
    Dev/demo reset.
    """
    session.execute(
        text(
            """
TRUNCATE TABLE
    cards,
    merchants,
    users
RESTART IDENTITY CASCADE;
"""
        )
    )
    session.commit()


def _enum_values(e: type) -> list:
    return list(e)


def seed_users(session: Session, cfg: SeedConfig) -> list[User]:
    """
    Creates unique usernames. If you re-run without --reset, it will skip collisions.
    """
    created: list[User] = []

    for i in range(cfg.users):
        username = f"user_{i:03d}"
        user = User(id=uuid.uuid4(), username=username)
        session.add(user)
        try:
            session.flush()
            created.append(user)
        except IntegrityError:
            session.rollback()
            existing = session.execute(
                select(User).where(User.username == username)
            ).scalar_one()
            created.append(existing)

    session.commit()
    return created


def seed_merchants(session: Session, cfg: SeedConfig) -> list[Merchant]:
    """
    Creates unique merchant names + assigns categories.
    """
    categories: Sequence[MerchantCategory] = _enum_values(MerchantCategory)
    created: list[Merchant] = []

    # Make names deterministic + unique
    base_names = [
        "QuickMart",
        "FuelStop",
        "ByteBuy",
        "SkyTravel",
        "CafeCorner",
        "HomeGoods",
        "PharmaPlus",
        "StyleStreet",
        "GameGalaxy",
        "FreshFarm",
    ]

    for i in range(cfg.merchants):
        name = f"{random.choice(base_names)}_{i:03d}"
        category = random.choice(categories)

        merchant = Merchant(id=uuid.uuid4(), name=name, category=category)
        session.add(merchant)
        try:
            session.flush()
            created.append(merchant)
        except IntegrityError:
            session.rollback()
            existing = session.execute(
                select(Merchant).where(Merchant.name == name)
            ).scalar_one()
            created.append(existing)

    session.commit()
    return created


def seed_cards(session: Session, cfg: SeedConfig, users: list[User]) -> list[Card]:
    """
    Creates cards for each user. Generates last4, brand, status, exp.
    """
    brands: Sequence[CardBrand] = _enum_values(CardBrand)
    statuses: Sequence[CardStatus] = _enum_values(CardStatus)

    created: list[Card] = []

    for user in users:
        for _ in range(cfg.cards_per_user):
            last4 = random.randint(0, 9999)
            brand = random.choice(brands)
            status = random.choice(statuses)
            exp_month = random.randint(1, 12)
            exp_year = random.randint(2026, 2032)

            card = Card(
                id=uuid.uuid4(),
                user_id=user.id,
                last4=last4,
                brand=brand,
                status=status,
                exp_month=exp_month,
                exp_year=exp_year,
            )
            session.add(card)
            created.append(card)

    session.commit()
    return created


def main() -> None:
    cfg = parse_args()
    random.seed(cfg.seed)

    session: Session = SessionLocal()
    try:
        if cfg.reset:
            reset_db(session)

        users = seed_users(session, cfg)
        merchants = seed_merchants(session, cfg)
        cards = seed_cards(session, cfg, users)

        print("Seed complete.")
        print(f"  Users:     {len(users)}")
        print(f"  Merchants: {len(merchants)}")
        print(f"  Cards:     {len(cards)}")
        print(f"  RNG seed:  {cfg.seed}")
        if cfg.reset:
            print("  Reset:     yes")
    finally:
        session.close()


if __name__ == "__main__":
    main()
