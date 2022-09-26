from otree.api import *


doc = """
Mini-Twitter
"""


class C(BaseConstants):
    NAME_IN_URL = 'twitter'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


def get_follower_ids(player: Player, including_myself):
    ids = [sub.follower_id_in_group for sub in Subscription.filter(leader=player)]
    if including_myself:
        ids.append(player.id_in_group)
    return ids


class Subscription(ExtraModel):
    # we store the player objects and id_in_group redundantly,
    # for convenience and performance

    leader = models.Link(Player)
    leader_id_in_group = models.IntegerField()

    follower = models.Link(Player)
    follower_id_in_group = models.IntegerField()


class Message(ExtraModel):
    player = models.Link(Player)
    player_id_in_group = models.IntegerField()
    group = models.Link(Group)
    text = models.LongStringField()


def to_dict(msg: Message):
    return dict(id_in_group=msg.player_id_in_group, text=msg.text,)


def live_method(player: Player, data):
    group = player.group
    my_id = player.id_in_group

    msg_type = data['type']

    if msg_type == 'write':
        text = data['text']
        msg = Message.create(player=player, player_id_in_group=my_id, text=text, group=group)
        followers = get_follower_ids(player, including_myself=True)
        return {follower: dict(messages=[to_dict(msg)]) for follower in followers}

    broadcast = {}
    if msg_type == 'toggle_follow':
        leader_id = data['id_in_group']
        leader = group.get_player_by_id(leader_id)
        subs = Subscription.filter(follower=player, leader=leader)
        if subs:
            [sub] = subs
            sub.delete()
        else:
            Subscription.create(
                leader=leader,
                leader_id_in_group=leader.id_in_group,
                follower=player,
                follower_id_in_group=my_id,
            )
        # notify the other person of the change to their followers
        broadcast[leader_id] = dict(followers=get_follower_ids(leader, including_myself=True))

    followers = get_follower_ids(player, including_myself=True)
    i_follow = [sub.leader_id_in_group for sub in Subscription.filter(follower=player)]
    i_dont_follow = [p.id_in_group for p in group.get_players() if p.id_in_group not in i_follow]
    unfiltered_messages = Message.filter(group=group)
    # i see my own messages in my feed
    my_feed_authors = i_follow + [my_id]
    messages = [to_dict(m) for m in unfiltered_messages if m.player_id_in_group in my_feed_authors]

    broadcast.update(
        {
            my_id: dict(
                full_load=True,
                followers=followers,
                i_follow=i_follow,
                i_dont_follow=i_dont_follow,
                messages=messages,
            )
        }
    )

    return broadcast


# PAGES
class MyPage(Page):
    live_method = live_method

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)


page_sequence = [MyPage]
