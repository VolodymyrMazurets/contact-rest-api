from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel
from datetime import datetime, timedelta


async def get_contacts(skip: int, limit: int, db: Session, query: str = None) -> List[Contact]:
    if query:
        return db.query(Contact).filter(
            (Contact.first_name.ilike(f"%{query}%")) |
            (Contact.last_name.ilike(f"%{query}%")) |
            (Contact.email.ilike(f"%{query}%"))
        ).offset(skip).limit(limit).all()
    else:
        return db.query(Contact).offset(skip).limit(limit).all()


async def get_upcoming_birthdays(skip: int, limit: int, db: Session) -> List[Contact]:
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.birthday.between(today, end_date)).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email,
                      phone=body.phone, birthday=body.birthday, additional_info=body.additional_info)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
