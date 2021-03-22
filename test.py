class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Вы должны указать заголовок'
    )

    def __str__(self):
        return self.title