from app.extensions import db

class BaseRepository:
    model = None

    @classmethod
    def get_by_id(cls, id):
        return cls.model.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def get_all_active(cls):
        return cls.model.query.filter_by(is_active=True).all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def update(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance

    @classmethod
    def delete(cls, instance):
        db.session.delete(instance)
        db.session.commit()

    @classmethod
    def save(cls, instance):
        db.session.add(instance)
        db.session.commit()
        return instance
