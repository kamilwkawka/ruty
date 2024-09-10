from celery import shared_task
from .matching_algorithm import match_users

def run_matching_task():
    match_users()