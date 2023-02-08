"""This simple CRUD application performs the following operations sequentially:
    1. Creates 100 new accounts with randomly generated IDs and randomly-computed balance amounts.
    2. Chooses two accounts at random and takes half of the money from the first and deposits it
     into the second.
    3. Chooses five accounts at random and deletes them.
"""

from math import floor
import os
import streamlit as st
import random
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from models import Account

# The code below inserts new accounts.


def create_accounts(session, num):
    """Create N new accounts with random account IDs and account balances.
    """
    st.write("Creating new accounts...")
    new_accounts = []
    while num > 0:
        account_id = uuid.uuid4()
        account_balance = floor(random.random()*1_000_000)
        new_accounts.append(Account(id=account_id, balance=account_balance))
        seen_account_ids.append(account_id)
        st.write(f"Created new account with id {account_id} and balance {account_balance}.")
        num = num - 1
    session.add_all(new_accounts)


def transfer_funds_randomly(session, one, two):
    """Transfer money between two accounts.
    """
    try:
        source = session.query(Account).filter(Account.id == one).one()
    except NoResultFound:
        st.write("No result was found")
    except MultipleResultsFound:
        st.write("Multiple results were found")
    dest = session.query(Account).filter(Account.id == two).first()
    st.write(f"Random account balances:\nAccount {one}: {source.balance}\nAccount {two}: {dest.balance}")

    amount = floor(source.balance/2)
    st.write(f"Transferring {amount} from account {one} to account {two}...")

    # Check balance of the first account.
    if source.balance < amount:
        raise ValueError(f"Insufficient funds in account {one}")
    source.balance -= amount
    dest.balance += amount

    st.write(f"Transfer complete.\nNew balances:\nAccount {one}: {source.balance}\nAccount {two}: {dest.balance}")


def delete_accounts(session, num):
    """Delete N existing accounts, at random.
    """
    st.write("Deleting existing accounts...")
    delete_ids = []
    while num > 0:
        delete_id = random.choice(seen_account_ids)
        delete_ids.append(delete_id)
        seen_account_ids.remove(delete_id)
        num = num - 1

    accounts = session.query(Account).filter(Account.id.in_(delete_ids)).all()

    for account in accounts:
        st.write(f"Deleted account {account.id}.")
        session.delete(account)


def initiate_table(connection):
    my_query = """
    CREATE TABLE accounts (id UUID PRIMARY KEY, balance INT8);
    """
    results = connection.execute(my_query).fetchall()


    # For cockroach demo:
    # DATABASE_URL=postgresql://demo:<demo_password>@127.0.0.1:26257?sslmode=require
    # For CockroachCloud:
    # DATABASE_URL=postgresql://<username>:<password>@<globalhost>:26257/<cluster_name>.defaultdb?sslmode=verify-full&sslrootcert=<certs_dir>/<ca.crt>
    # db_uri = os.environ['DATABASE_URL'].replace("postgresql://", "cockroachdb://")

# DATABASE_URL = "cockroachdb://arch:f54qpucS7ci4HSm9yZtItg@arch-test1-3423.6xw.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=root.crt"
DATABASE_URL = "cockroachdb://arch:f54qpucS7ci4HSm9yZtItg@arch-test1-3423.6xw.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"
db_uri = DATABASE_URL.replace("postgresql://", "cockroachdb://")

try:
    engine = create_engine(db_uri, connect_args={"application_name":"docs_simplecrud_sqlalchemy"})
except Exception as e:
    st.write("Failed to connect to database.")
    st.write(f"{e}")

# initiate_table(engine.connect())

st.title("KWAP 2023 ESG Game")
st.subheader("Achieving long-term sustainable investment outcomes")

if st.button("Click"):
    seen_account_ids = []

    run_transaction(sessionmaker(bind=engine),
                    lambda s: create_accounts(s, 10))

    from_id = random.choice(seen_account_ids)
    to_id = random.choice([id for id in seen_account_ids if id != from_id])

    run_transaction(sessionmaker(bind=engine),
                    lambda s: transfer_funds_randomly(s, from_id, to_id))

    run_transaction(sessionmaker(bind=engine), lambda s: delete_accounts(s, 5))
    
    st.write("Done running")
