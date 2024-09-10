from .models import User, surveyResponse, Group, GroupMembership
from django.db.models import Q
from itertools import combinations
from collections import defaultdict

def calculate_similarity(user1, user2):
    score = 0
    total = 3
    if user1.surveyreponse.question_1 == user2.surveyresponse.question_1:
        score+=1
    if user1.surveyreponse.question_2 == user2.surveyresponse.question_2:
        score+=1
    if user1.surveyreponse.question_3 == user2.surveyresponse.question_3:
        score+=1
    return score / total

def match_users():

    users = User.objects.filter(surveyresponse__isnull=False).exclude(
        group_membership__isnull=False
    )
    
    if len(users) < 4:
        return
    
    sim_scores = defaultdict(dict)
    for user1, user2 in combinations(users, 2):
        sim = calculate_similarity(user1, user2)
        sim_scores[user1.id][user2.id] = sim
        sim_scores[user2.id][user1.id] = sim
    
    groups = []
    users_ids = set(user.id for user in users)

    while len(users_ids) >= 4:
        user_id = users_ids.pop()
        similar_users = sorted(sim_scores[user_id].items(), key=lambda x: x[1], reverse=True)
        group = [user_id]
        for similar_user_id, score in similar_users:
            if similar_user_id in users_ids:
                group.append(similar_user_id)
                if len(group) == 4:
                    break
            if len(group) == 4:
                groups.append(group)
                users_ids -=  set(group[1:])
            else:
                break

    for group_ids in groups:
        group = Group.objects.create(name=f"Group {group_ids[0]}")
        for uid in group_ids:
            user = User.objects.get(id=uid)
            GroupMembership.objects.create(user=user, group=group)
    