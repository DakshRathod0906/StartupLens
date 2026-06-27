from django.db import models

class StartupIdeaQuerySet(models.QuerySet):
    def active(self):
        from .constants import StartupIdeaStatus
        return self.exclude(status=StartupIdeaStatus.ARCHIVED)
        
    def archived(self):
        from .constants import StartupIdeaStatus
        return self.filter(status=StartupIdeaStatus.ARCHIVED)
        
    def published(self):
        from .constants import StartupIdeaStatus
        return self.filter(status=StartupIdeaStatus.PUBLISHED)
        
    def drafts(self):
        from .constants import StartupIdeaStatus
        return self.filter(status=StartupIdeaStatus.DRAFT)
        
    def owned_by(self, user):
        return self.filter(owner=user)
        
    def search(self, query=None, industry_id=None, status=None, stage=None):
        qs = self
        if query:
            qs = qs.filter(
                models.Q(title__icontains=query) | 
                models.Q(short_description__icontains=query)
            )
        if industry_id:
            qs = qs.filter(industry_id=industry_id)
        if status:
            qs = qs.filter(status=status)
        if stage:
            qs = qs.filter(startup_stage=stage)
        return qs

class StartupIdeaManager(models.Manager):
    def get_queryset(self):
        return StartupIdeaQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def active(self): return self.get_queryset().active()
    def archived(self): return self.get_queryset().archived()
    def published(self): return self.get_queryset().published()
    def drafts(self): return self.get_queryset().drafts()
    def owned_by(self, user): return self.get_queryset().owned_by(user)
    def search(self, *args, **kwargs): return self.get_queryset().search(*args, **kwargs)
        
class StartupIdeaAllManager(models.Manager):
    def get_queryset(self):
        return StartupIdeaQuerySet(self.model, using=self._db)

    def active(self): return self.get_queryset().active()
    def archived(self): return self.get_queryset().archived()
    def published(self): return self.get_queryset().published()
    def drafts(self): return self.get_queryset().drafts()
    def owned_by(self, user): return self.get_queryset().owned_by(user)
    def search(self, *args, **kwargs): return self.get_queryset().search(*args, **kwargs)
