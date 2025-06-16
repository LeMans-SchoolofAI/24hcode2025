from django.db import models

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    response = models.TextField()
    def __str__(self):
        return f"Conversation {self.id}"
    

class User_input(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField(default=0)
    message = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    def __str__(self):
        return f"User input {self.message}"
    
class Ai_response(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField(default=0)
    response = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    def __str__(self):
        return f"Ai response {self.response}"
