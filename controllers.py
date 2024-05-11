from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import or_
import datetime
from sqlalchemy.exc import IntegrityError

# Repositories functions
def get_repository(db: Session, repository_id: int):
    return db.query(models.Repository).filter(models.Repository.id_repository == repository_id).first()

def get_repository_by_id(db: Session, repository_name: str):
    return db.query(models.Repository).filter(models.Repository.name_repository == repository_name).first()

def get_repository_by_name(db: Session, repository_name: str):
    return db.query(models.Repository).filter(models.Repository.name_repository == repository_name).first()

def get_repositories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Repository).offset(skip).limit(limit).all()

def create_repository(db: Session, repository: schemas.RepositoryCreate):
    db_repository = models.Repository(id_repository=repository.id_repository, name_repository=repository.name_repository, url_repository=repository.url_repository)
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

# Users functions
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id_user == user_id).first()

def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.name_user == user_name).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id_user == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = None

    # Verifica si ya existe un usuario con el mismo id en la base de datos
    existing_user = db.query(models.User).filter(models.User.id_user == user.id_user).first()
    if not existing_user:
        db_user = models.User(id_user= user.id_user, login_user=user.login_user, experience=user.experience, id_repository=user.id_repository)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    return db_user

# Commits functions
def get_commit(db: Session, commit_id: int):
    return db.query(models.Commit).filter(models.Commit.id_commit == commit_id).first()

def get_commit_by_id(db: Session, commit_id: int):
    return db.query(models.Commit).filter(models.Commit.id_commit == commit_id).first()

def get_commits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Commit).offset(skip).limit(limit).all()

def create_commit(db: Session, commit: schemas.CommitCreate):
    db_commit = models.Commit(id_commit=commit.id_commit ,created_at_commit=commit.created_at_commit, id_user=commit.id_user, id_repository=commit.id_repository)
    db.add(db_commit)
    db.commit()
    db.refresh(db_commit)
    return db_commit

# Pull Requests functions
def get_pull_request(db: Session, pull_request_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_pull == pull_request_id).first()

def get_pull_request_by_id(db: Session, pull_request_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_pull == pull_request_id).first()

def get_pull_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PullRequest).offset(skip).limit(limit).all()

def create_pull_request(db: Session, pull_request: schemas.PullRequestCreate):
    try:
        db_pull_request = models.PullRequest(id_pull=pull_request.id_pull, name=pull_request.name, created_at=pull_request.created_at, closed_at=pull_request.closed_at,status=pull_request.status, id_user=pull_request.id_user, id_repository=pull_request.id_repository, id_commit=pull_request.id_commit)
        db.add(db_pull_request)
        db.commit()
        db.refresh(db_pull_request)
        return db_pull_request
    except IntegrityError:
        db.rollback()
        pull_request.id_commit = None  # Configurar id_commit en None
        db_pull_request = models.PullRequest(id_pull=pull_request.id_pull, name=pull_request.name, created_at=pull_request.created_at, closed_at=pull_request.closed_at,status=pull_request.status, id_user=pull_request.id_user, id_repository=pull_request.id_repository, id_commit=pull_request.id_commit)
        db.add(db_pull_request)
        db.commit()
        db.refresh(db_pull_request)
        return db_pull_request

# Issues functions
def get_issue(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id_issue == issue_id).first()

def get_issue_by_id(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id_issue == issue_id).first()

def get_issues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Issue).offset(skip).limit(limit).all()

def create_issue(db: Session, issue: schemas.IssueCreate):
    db_issue = models.Issue(id_issue=issue.id_issue, name=issue.name, created_at=issue.created_at, closed_at=issue.closed_at, resolution_time=issue.resolution_time, id_user=issue.id_user, id_resolution_commit=issue.id_resolution_commit, id_repository=issue.id_repository)
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue

# Functions for the relationships between tables
def get_commits_by_user(db: Session, user_id: int):
    return db.query(models.Commit).filter(models.Commit.id_user == user_id).all()

def get_pull_requests_by_user(db: Session, user_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_user == user_id).all()

def get_issues_by_user(db: Session, user_id: int):
    return db.query(models.Issue).filter(models.Issue.id_user == user_id).all()

def get_commits_by_repository(db: Session, repository_id: int):
    return db.query(models.Commit).filter(models.Commit.id_repository == repository_id).all()

def get_pull_requests_by_repository(db: Session, repository_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_repository == repository_id).all()

def get_issues_by_repository(db: Session, repository_id: int):
    return db.query(models.Issue).filter(models.Issue.id_repository == repository_id).all()

def get_commits_by_user_and_repository(db: Session, user_id: int, repository_id: int):
    return db.query(models.Commit).filter(models.Commit.id_user == user_id, models.Commit.id_repository == repository_id).all()

def get_pull_requests_by_user_and_repository(db: Session, user_id: int, repository_id: int):
    return db.query(models.PullRequest).filter(models.PullRequest.id_user == user_id, models.PullRequest.id_repository == repository_id).all()

def get_issues_by_user_and_repository(db: Session, user_id: int, repository_id: int):
    return db.query(models.Issue).filter(models.Issue.id_user == user_id, models.Issue.id_repository == repository_id).all()

def get_commits_by_user_and_repository_and_date(db: Session, user_id: int, repository_id: int, date: datetime):
    return db.query(models.Commit).filter(models.Commit.id_user == user_id, models.Commit.id_repository == repository_id, models.Commit.created_at_commit >= date).all()

# Define Experience for all the users
def calculate_experience(db:Session):

    # Obtenemos todos los usuarios
    users = db.query(models.User).all()

    # Iteramos sobre todos los usuarios
    for user in users:
        current_time = datetime.datetime.now()

        # Obtenemos la fecha de su primer commit
        first_commit = db.query(models.Commit).filter(models.Commit.id_user == user.id_user).order_by(models.Commit.created_at_commit).first()
        if first_commit:
            first_commit_date = first_commit.created_at_commit
        else:
            first_commit_date = current_time  # Si no tiene commits, usamos la fecha actual
        
        # Obtenemos la fecha de su primer pull request cerrado
        first_pr = db.query(models.PullRequest).filter(models.PullRequest.id_user == user.id_user, models.PullRequest.status == 'closed').order_by(models.PullRequest.closed_at).first()
        if first_pr:
            first_pr_date = first_pr.closed_at
        else:
            first_pr_date = current_time  # Si no tiene pull requests cerrados, usamos la fecha actual
        
        # Obtenemos la fecha de su primer issue cerrado
        first_issue = db.query(models.Issue).filter(models.Issue.id_user == user.id_user, models.Issue.closed_at.isnot(None)).order_by(models.Issue.closed_at).first()
        if first_issue:
            first_issue_date = first_issue.closed_at
        else:
            first_issue_date = current_time  # Si no tiene issues cerrados, usamos la fecha actual
        
        # Calculamos la diferencia en meses desde cada primera contribución hasta ahora
        commit_experience = (current_time - first_commit_date).days // 30
        pr_experience = (current_time - first_pr_date).days // 30
        issue_experience = (current_time - first_issue_date).days // 30

        # Calculamos la experiencia final tomando el maximo de los tres
        experience = max(commit_experience, pr_experience, issue_experience)

        # Asignamos la categoría de experiencia según tus criterios
        if experience <= 3:
            experience_category = "onboarded"
        elif 6 <= experience <= 12:
            experience_category = "experienced"
        else:
            experience_category = "veteran"

        # Actualizamos el campo 'experience' en la base de datos
        user.experience = experience_category
        db.commit() 

# Define progreso de carga de datos
def insert_progress(db: Session, message: str, percentage: int = None):
    progress = models.Progress(message=message, percentage=percentage)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress

# Actualizar progreso de carga de datos
def update_progress(db: Session, progress_id: int, message: str = None, percentage: int = None):
    progress = db.query(models.Progress).filter(models.Progress.id_progress == progress_id).first()
    if progress:
        progress.message = message
        progress.percentage = percentage
        db.commit()
        db.refresh(progress)
    return progress

# Obtener progreso de carga de datos
def get_latest_progress(db: Session):
    return db.query(models.Progress).order_by(models.Progress.id_progress.desc()).first() or models.Progress(percentage=0, message="Starting repository data download...")

# Borra todos los datos de la base de datos
def delete_all_data(db: Session):

    # Borra todos los datos de las tablas
    # for table in reversed(models.Base.metadata.sorted_tables):
    #     db.execute(table.delete())

    try:
        print("Deleting all data...")
        # Borra todos los datos de las tablas
        models.Base.metadata.drop_all(bind=db.bind)

        # Crea todas las tablas de la base de datos
        models.Base.metadata.create_all(bind=db.bind)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise
    
