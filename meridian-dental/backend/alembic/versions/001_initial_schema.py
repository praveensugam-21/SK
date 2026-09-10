"""initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-05-20 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # clinics
    op.create_table('clinics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('logo_url', sa.String(length=500), nullable=True),
        sa.Column('settings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # users
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
        sa.Column('password_hash', sa.String(length=200), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=False),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('specialization', sa.String(length=200), nullable=True),
        sa.Column('license_number', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default=sa.text('0')),
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # patients
    op.create_table('patients',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id_display', sa.String(length=50), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('emergency_contact_name', sa.String(length=200), nullable=True),
        sa.Column('emergency_contact_phone', sa.String(length=20), nullable=True),
        sa.Column('blood_group', sa.String(length=5), nullable=True),
        sa.Column('allergies', sa.Text(), nullable=True),
        sa.Column('medical_history', sa.Text(), nullable=True),
        sa.Column('current_medications', sa.Text(), nullable=True),
        sa.Column('insurance_provider', sa.String(length=200), nullable=True),
        sa.Column('insurance_id', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, default='active'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('patient_id_display', 'clinic_id')
    )
    op.create_index(op.f('ix_patients_full_name'), 'patients', ['full_name'], unique=False)
    op.create_index(op.f('ix_patients_phone'), 'patients', ['phone'], unique=False)
    op.create_index(op.f('ix_patients_patient_id_display'), 'patients', ['patient_id_display'], unique=False)
    
    # appointments
    op.create_table('appointments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dentist_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('appointment_type', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, default='scheduled'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('cancellation_reason', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ),
        sa.ForeignKeyConstraint(['dentist_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_appointments_date'), 'appointments', ['date'], unique=False)

    # teeth_records
    op.create_table('teeth_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tooth_number', sa.Integer(), nullable=False),
        sa.Column('condition', sa.String(length=100), nullable=False),
        sa.Column('surfaces', postgresql.JSONB(), nullable=True),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('treatment', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('updated_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('patient_id', 'tooth_number')
    )
    
    # tooth_history
    op.create_table('tooth_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('record_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('previous_condition', sa.String(length=100), nullable=True),
        sa.Column('new_condition', sa.String(length=100), nullable=False),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('treatment', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('changed_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('changed_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['record_id'], ['teeth_records.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # treatment_plans
    op.create_table('treatment_plans',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dentist_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, default='planned'),
        sa.Column('total_estimated_cost', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ),
        sa.ForeignKeyConstraint(['dentist_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # treatments
    op.create_table('treatments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plan_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dentist_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tooth_number', sa.Integer(), nullable=True),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('treatment_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cost', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('status', sa.String(length=20), nullable=False, default='planned'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['dentist_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.ForeignKeyConstraint(['plan_id'], ['treatment_plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # invoices
    op.create_table('invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invoice_number', sa.String(length=50), nullable=False),
        sa.Column('invoice_date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
        sa.Column('due_date', sa.Date(), nullable=False),
        sa.Column('subtotal', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('discount_amount', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('tax_amount', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('total_amount', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('amount_paid', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('balance', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('status', sa.String(length=20), nullable=False, default='pending'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invoice_number', 'clinic_id')
    )
    op.create_index(op.f('ix_invoices_invoice_number'), 'invoices', ['invoice_number'], unique=False)
    
    # invoice_items
    op.create_table('invoice_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=False),
        sa.Column('treatment_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False, default=1),
        sa.Column('unit_price', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('discount', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.ForeignKeyConstraint(['treatment_id'], ['treatments.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # payments
    op.create_table('payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('payment_method', sa.String(length=50), nullable=False),
        sa.Column('transaction_reference', sa.String(length=200), nullable=True),
        sa.Column('payment_date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
        sa.Column('received_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['invoice_id'], ['invoices.id'], ),
        sa.ForeignKeyConstraint(['received_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # prescriptions
    op.create_table('prescriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('dentist_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['dentist_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # prescription_items
    op.create_table('prescription_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('prescription_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('medication', sa.String(length=200), nullable=False),
        sa.Column('dosage', sa.String(length=100), nullable=True),
        sa.Column('frequency', sa.String(length=100), nullable=True),
        sa.Column('duration', sa.String(length=100), nullable=True),
        sa.Column('instructions', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['prescription_id'], ['prescriptions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # documents
    op.create_table('documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('filename', sa.String(length=500), nullable=False),
        sa.Column('original_filename', sa.String(length=500), nullable=False),
        sa.Column('file_key', sa.String(length=500), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False, default='other'),
        sa.Column('uploaded_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # notes
    op.create_table('notes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('author_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('note_type', sa.String(length=50), nullable=False, default='general'),
        sa.Column('is_clinical', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # audit_logs
    op.create_table('audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('entity_type', sa.String(length=100), nullable=False),
        sa.Column('entity_id', sa.String(length=100), nullable=True),
        sa.Column('old_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('new_values', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # notifications
    op.create_table('notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('clinic_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('notification_type', sa.String(length=50), nullable=False, default='system'),
        sa.Column('is_read', sa.Boolean(), nullable=False, default=False),
        sa.Column('action_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['clinic_id'], ['clinics.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # patient_timeline
    op.create_table('patient_timeline',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('event_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('patient_timeline')
    op.drop_table('notifications')
    op.drop_table('audit_logs')
    op.drop_table('notes')
    op.drop_table('documents')
    op.drop_table('prescription_items')
    op.drop_table('prescriptions')
    op.drop_table('payments')
    op.drop_table('invoice_items')
    op.drop_table('invoices')
    op.drop_table('treatments')
    op.drop_table('treatment_plans')
    op.drop_table('tooth_history')
    op.drop_table('teeth_records')
    op.drop_table('appointments')
    op.drop_table('patients')
    op.drop_table('users')
    op.drop_table('clinics')
