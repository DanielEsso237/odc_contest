from django.db import models
from accounts.models import User

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de l'événement")
    description = models.TextField(verbose_name="Description")
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'modo'}, related_name='created_events', verbose_name="Créé par")

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"

    def __str__(self):
        return self.title

class Trial(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='trials', verbose_name="Événement")
    title = models.CharField(max_length=100, verbose_name="Titre de l'épreuve (ex. Cosplay)")
    description = models.TextField(blank=True, verbose_name="Description de l'épreuve")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'apparition")

    class Meta:
        verbose_name = "Trial (Épreuve)"
        verbose_name_plural = "Trials (Épreuves)"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.event.title})"

class Competitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'participant'}, related_name='competitor_profile', verbose_name="Concurrente")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='competitors', verbose_name="Événement")
    registered_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'modo'}, related_name='registered_competitors', verbose_name="Enregistré par")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")

    class Meta:
        verbose_name = "Concurrente"
        verbose_name_plural = "Concurrentes"
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Submission(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='submissions', verbose_name="Concurrente")
    trial = models.ForeignKey(Trial, on_delete=models.CASCADE, related_name='submissions', verbose_name="Épreuve")
    description = models.TextField(verbose_name="Description")
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'modo'}, related_name='published_submissions', verbose_name="Publié par", null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    is_published = models.BooleanField(default=False, verbose_name="Publié ?")
    
    # IMPORTANT: Le champ 'media' a été supprimé d'ici

    class Meta:
        verbose_name = "Soumission"
        verbose_name_plural = "Soumissions"
        unique_together = ('competitor', 'trial')

    def __str__(self):
        return f"{self.competitor.user.username} - {self.trial.title}"

class SubmissionMedia(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='media_files', verbose_name="Soumission")
    media = models.FileField(upload_to='submissions/', verbose_name="Média (photo ou vidéo)", help_text="Téléchargez une photo (.jpg, .jpeg, .png) ou une vidéo (.mp4, .mov)")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    def clean(self):
        import os
        from django.core.exceptions import ValidationError
        if self.media:
            file_extension = os.path.splitext(self.media.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']
            if file_extension not in valid_extensions:
                raise ValidationError("Seules les extensions .jpg, .jpeg, .png, .mp4 et .mov sont autorisées.")

    class Meta:
        verbose_name = "Média de soumission"
        verbose_name_plural = "Médias de soumission"
        ordering = ['order']

    def __str__(self):
        return f"Média pour {self.submission}"

    def is_video(self):
        """Vérifie si le fichier est une vidéo"""
        if self.media:
            import os
            file_extension = os.path.splitext(self.media.name)[1].lower()
            return file_extension in ['.mp4', '.mov']
        return False

class Vote(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['member', 'participant']}, related_name='votes', verbose_name="Membre votant")
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='votes', verbose_name="Soumission votée")
    voted_at = models.DateTimeField(auto_now_add=True, verbose_name="Date du vote")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        unique_together = ('member', 'submission')

    def __str__(self):
        return f"{self.member.username} a voté pour {self.submission.competitor.user.username}"