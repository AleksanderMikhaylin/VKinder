import sqlalchemy as sq
from sqlalchemy.orm import relationship
from VKinder.model.base import Base


class User(Base):
    __tablename__ = 'users'

    id = sq.Column(sq.Integer, primary_key=True, index=True)
    token = sq.Column(sq.String)
    # candidate_id = sq.Column(sq.Integer, sq.ForeignKey('candidates.id'))
    # candidates = relationship('Candidate', back_populates='users')


class Candidate(Base):
    __tablename__ = 'candidates'

    id = sq.Column(sq.Integer, primary_key=True, index=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    screen_name = sq.Column(sq.String)
    # photo_id = sq.Column(sq.String, sq.ForeignKey('photos.id'))
    # photos = relationship('Photo', back_populates='candidates')
    # users = relationship('User', secondary=candidates_for_users, backref='candidates')


class Photo(Base):
    __tablename__ = 'photos'

    id = sq.Column(sq.Integer, primary_key=True)
    photo_id = sq.Column(sq.String)
    candidate_id = sq.Column(sq.Integer)
    likes_count = sq.Column(sq.Integer)
    comments_count = sq.Column(sq.Integer)
    # candidates = relationship('Candidate', back_populates='photos')


class ReviewedCandidates(Base):
    __tablename__ = 'reviewed_candidates'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer)
    candidate_id = sq.Column(sq.Integer)


class CandidatesForUser(Base):
    __tablename__ = 'candidates_for_users'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer)
    candidate_id = sq.Column(sq.Integer)
