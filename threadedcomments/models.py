from django.db import models
from django.contrib.comments.models import Comment
from django.conf import settings

PATH_SEPARATOR = getattr(settings, 'COMMENT_PATH_SEPARATOR', '/')
PATH_DIGITS = getattr(settings, 'COMMENT_PATH_DIGITS', 10)

class ThreadedComment(Comment):
    parent = models.ForeignKey('self', null=True, blank=True, default=None,
        related_name='children')
    tree_path = models.TextField(null=True, blank=True, db_index=True)
    
    def _get_depth(self):
        return len(self.tree_path.split(PATH_SEPARATOR))
    depth = property(_get_depth)
    
    def save(self, *args, **kwargs):
        super(ThreadedComment, self).save(*args, **kwargs)
        path_list = [unicode(self.pk).zfill(PATH_DIGITS)]
        if self.parent:
            path_list.append(self.parent.tree_path)
        self.tree_path = PATH_SEPARATOR.join(path_list)
        super(ThreadedComment, self).save(*args, **kwargs)
