from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="customer"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("slots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("service_name", sa.String(120), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(200), nullable=False, server_default="Main branch"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_index("ix_slots_starts_at", "slots", ["starts_at"])
    op.create_table("bookings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("customer_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("slot_id", sa.Integer(), sa.ForeignKey("slots.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="confirmed"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index("uq_active_booking_slot", "bookings", ["slot_id"], unique=True,
                    postgresql_where=sa.text("status = 'confirmed'"))
    op.create_index("ix_booking_customer_created", "bookings", ["customer_id", "created_at"])

def downgrade():
    op.drop_index("ix_booking_customer_created", table_name="bookings")
    op.drop_index("uq_active_booking_slot", table_name="bookings")
    op.drop_table("bookings")
    op.drop_index("ix_slots_starts_at", table_name="slots")
    op.drop_table("slots")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
