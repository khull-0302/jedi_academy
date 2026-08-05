from db import db

padawans_courses_association_table = db.Table(
    "PadawansCoursesAssociation",
    db.Model.metadata,
    db.Column("padawan_id", db.ForeignKey("Padawans.padawan_id", ondelete="CASCADE"), primary_key=True),
    db.Column("course_id", db.ForeignKey("Courses.course_id", ondelete="CASCADE"), primary_key=True)
)