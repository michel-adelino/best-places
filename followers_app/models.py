from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Follower(models.Model):
    """ Followers table:
            - user = the person being followed (target)
            - follower = the user following the user
    """
    user = models.ForeignKey(User, related_name='folowee',
                             on_delete=models.SET_NULL, null=True)
    follower = models.ForeignKey(User, related_name='follower',
                                 on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.follower} is following {self.user}'
