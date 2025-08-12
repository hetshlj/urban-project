-- Database schema for service marketplace platform (MySQL)

-- 1. users
drop table if exists users;
create table users (
    id int auto_increment primary key,
    name varchar(100) not null,
    email varchar(100) not null unique,
    password_hash varchar(255) not null,
    phone varchar(20),
    user_type enum('customer','provider','admin') not null,
    profile_image varchar(255),
    status varchar(20) default 'active',
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp
);

-- 2. providers
drop table if exists providers;
create table providers (
    id int auto_increment primary key,
    user_id int not null,
    business_name varchar(100),
    business_address varchar(255),
    service_area varchar(100),
    license_number varchar(50),
    rating decimal(2,1) default 0.0,
    about text,
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp,
    foreign key (user_id) references users(id)
);

-- 3. categories
drop table if exists categories;
create table categories (
    id int auto_increment primary key,
    name varchar(100) not null,
    parent_id int,
    icon varchar(100),
    created_at datetime default current_timestamp,
    foreign key (parent_id) references categories(id)
);

-- 4. services
drop table if exists services;
create table services (
    id int auto_increment primary key,
    provider_id int not null,
    category_id int not null,
    title varchar(150) not null,
    description text,
    price decimal(10,2) not null,
    duration int,
    location varchar(255),
    status varchar(20) default 'active',
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp,
    foreign key (provider_id) references providers(id),
    foreign key (category_id) references categories(id)
);

-- 5. bookings
drop table if exists bookings;
create table bookings (
    id int auto_increment primary key,
    service_id int not null,
    customer_id int not null,
    provider_id int not null,
    booking_date datetime not null,
    status enum('pending','confirmed','completed','cancelled') default 'pending',
    payment_status enum('paid','unpaid') default 'unpaid',
    total_amount decimal(10,2),
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id),
    foreign key (customer_id) references users(id),
    foreign key (provider_id) references providers(id)
);

-- 6. reviews
drop table if exists reviews;
create table reviews (
    id int auto_increment primary key,
    booking_id int not null,
    reviewer_id int not null,
    rating int not null,
    comment text,
    created_at datetime default current_timestamp,
    foreign key (booking_id) references bookings(id),
    foreign key (reviewer_id) references users(id)
);

-- 7. payments
drop table if exists payments;
create table payments (
    id int auto_increment primary key,
    booking_id int not null,
    amount decimal(10,2) not null,
    payment_method varchar(50),
    payment_date datetime,
    status varchar(20),
    foreign key (booking_id) references bookings(id)
);

-- 8. blogs
drop table if exists blogs;
create table blogs (
    id int auto_increment primary key,
    title varchar(200) not null,
    content text,
    author_id int not null,
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp,
    foreign key (author_id) references users(id)
);

-- 9. notifications
drop table if exists notifications;
create table notifications (
    id int auto_increment primary key,
    user_id int not null,
    message text not null,
    is_read boolean default false,
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(id)
);

-- 10. wallets
drop table if exists wallets;
create table wallets (
    id int auto_increment primary key,
    user_id int not null,
    balance decimal(10,2) default 0.0,
    updated_at datetime default current_timestamp on update current_timestamp,
    foreign key (user_id) references users(id)
);

-- 11. transactions
drop table if exists transactions;
create table transactions (
    id int auto_increment primary key,
    wallet_id int not null,
    amount decimal(10,2) not null,
    type enum('credit','debit') not null,
    description varchar(255),
    created_at datetime default current_timestamp,
    foreign key (wallet_id) references wallets(id)
);

-- 12. staff
drop table if exists staff;
create table staff (
    id int auto_increment primary key,
    provider_id int not null,
    name varchar(100) not null,
    role varchar(50),
    contact varchar(50),
    created_at datetime default current_timestamp,
    foreign key (provider_id) references providers(id)
);

-- 13. devices
drop table if exists devices;
create table devices (
    id int auto_increment primary key,
    user_id int not null,
    device_token varchar(255),
    device_type varchar(50),
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(id)
);

-- 14. chat_rooms
drop table if exists chat_rooms;
create table chat_rooms (
    id int auto_increment primary key,
    customer_id int not null,
    provider_id int not null,
    created_at datetime default current_timestamp,
    foreign key (customer_id) references users(id),
    foreign key (provider_id) references providers(id)
);

-- 15. chat_messages
drop table if exists chat_messages;
create table chat_messages (
    id int auto_increment primary key,
    room_id int not null,
    sender_id int not null,
    message text not null,
    sent_at datetime default current_timestamp,
    is_read boolean default false,
    foreign key (room_id) references chat_rooms(id),
    foreign key (sender_id) references users(id)
);

-- 16. admin_roles
drop table if exists admin_roles;
create table admin_roles (
    id int auto_increment primary key,
    name varchar(50) not null,
    description varchar(255)
);

drop table if exists admin_permissions;
create table admin_permissions (
    id int auto_increment primary key,
    name varchar(50) not null,
    description varchar(255)
);

drop table if exists admin_role_permissions;
create table admin_role_permissions (
    id int auto_increment primary key,
    role_id int not null,
    permission_id int not null,
    foreign key (role_id) references admin_roles(id),
    foreign key (permission_id) references admin_permissions(id)
);

drop table if exists admin_user_roles;
create table admin_user_roles (
    id int auto_increment primary key,
    user_id int not null,
    role_id int not null,
    foreign key (user_id) references users(id),
    foreign key (role_id) references admin_roles(id)
);

drop table if exists admin_activity_logs;
create table admin_activity_logs (
    id int auto_increment primary key,
    admin_id int not null,
    action varchar(100) not null,
    details text,
    created_at datetime default current_timestamp,
    foreign key (admin_id) references users(id)
);

-- Add created_at and updated_at to all tables for consistency

alter table admin_roles add column created_at datetime default current_timestamp;
alter table admin_roles add column updated_at datetime default current_timestamp on update current_timestamp;

alter table admin_permissions add column created_at datetime default current_timestamp;
alter table admin_permissions add column updated_at datetime default current_timestamp on update current_timestamp;

alter table admin_role_permissions add column created_at datetime default current_timestamp;
alter table admin_role_permissions add column updated_at datetime default current_timestamp on update current_timestamp;

alter table admin_user_roles add column created_at datetime default current_timestamp;
alter table admin_user_roles add column updated_at datetime default current_timestamp on update current_timestamp;

alter table admin_activity_logs add column updated_at datetime default current_timestamp on update current_timestamp;
create table service_addons (
    id int auto_increment primary key,
    service_id int not null,
    name varchar(100) not null,
    price decimal(10,2) not null,
    duration int,
    foreign key (service_id) references services(id)
);
create table provider_availability (
    id int auto_increment primary key,
    provider_id int not null,
    day_of_week enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') not null,
    start_time time not null,
    end_time time not null,
    is_available boolean default true,
    foreign key (provider_id) references providers(id)
);
create table user_addresses (
    id int auto_increment primary key,
    user_id int not null,
    label varchar(50),
    address_line varchar(255),
    city varchar(100),
    state varchar(100),
    postal_code varchar(20),
    latitude decimal(10,6),
    longitude decimal(10,6),
    is_default boolean default false,
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(id)
);
create table coupons (
    id int auto_increment primary key,
    code varchar(50) unique not null,
    description varchar(255),
    discount_type enum('percent','fixed') not null,
    discount_value decimal(10,2) not null,
    valid_from datetime,
    valid_until datetime,
    usage_limit int,
    created_at datetime default current_timestamp
);

create table booking_coupons (
    id int auto_increment primary key,
    booking_id int not null,
    coupon_id int not null,
    discount_applied decimal(10,2),
    foreign key (booking_id) references bookings(id),
    foreign key (coupon_id) references coupons(id)
);
create table service_images (
    id int auto_increment primary key,
    service_id int not null,
    image_url varchar(255) not null,
    is_primary boolean default false,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id)
);
create table service_faqs (
    id int auto_increment primary key,
    service_id int not null,
    question varchar(255) not null,
    answer text not null,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id)
);
create table service_tags (
    id int auto_increment primary key,
    service_id int not null,
    tag varchar(50) not null,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id)
);
create table service_promotions (
    id int auto_increment primary key,
    service_id int not null,
    promotion_type enum('discount','offer') not null,
    description varchar(255),
    start_date datetime,
    end_date datetime,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id)
);
create table service_questions (
    id int auto_increment primary key,
    service_id int not null,
    question varchar(255) not null,
    answer text,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id)
);
create table service_bookmarks (
    id int auto_increment primary key,
    user_id int not null,
    service_id int not null,
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(id),
    foreign key (service_id) references services(id)
);
create table booking_logs (
    id int auto_increment primary key,
    booking_id int not null,
    status enum('pending','confirmed','completed','cancelled') not null,
    changed_by int,
    changed_at datetime default current_timestamp,
    remarks text,
    foreign key (booking_id) references bookings(id),
    foreign key (changed_by) references users(id)
);
create table service_notifications (
    id int auto_increment primary key,
    service_id int not null,
    user_id int not null,
    message text not null,
    is_read boolean default false,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id),
    foreign key (user_id) references users(id)
);
create table service_statistics (
    id int auto_increment primary key,
    service_id int not null,
    views int default 0,
    bookings int default 0,
    ratings int default 0,
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp,
    foreign key (service_id) references services(id)
);
create table service_questions_answers (
    id int auto_increment primary key,
    question_id int not null,
    answer text not null,
    answered_by int not null,
    created_at datetime default current_timestamp,
    foreign key (question_id) references service_questions(id),
    foreign key (answered_by) references users(id)
);
create table service_wishlist (
    id int auto_increment primary key,
    user_id int not null,
    service_id int not null,
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(id),
    foreign key (service_id) references services(id)
);
create table service_subscriptions (
    id int auto_increment primary key,
    user_id int not null,
    service_id int not null,
    subscription_type enum('monthly','yearly') not null,
    start_date datetime not null,
    end_date datetime not null,
    status enum('active','inactive','cancelled') default 'active',
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(id),
    foreign key (service_id) references services(id)
);
create table service_feedback (
    id int auto_increment primary key,
    service_id int not null,
    user_id int not null,
    feedback text not null,
    rating int not null,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id),
    foreign key (user_id) references users(id)
);
create table service_notifications_settings (
    id int auto_increment primary key,
    user_id int not null,
    email_notifications boolean default true,
    sms_notifications boolean default false,
    push_notifications boolean default true,
    created_at datetime default current_timestamp,
    foreign key (user_id) references users(id)
);
create table service_referrals (
    id int auto_increment primary key,
    referrer_id int not null,
    referred_email varchar(100) not null,
    referral_code varchar(50) unique not null,
    status enum('pending','accepted','rejected') default 'pending',
    created_at datetime default current_timestamp,
    foreign key (referrer_id) references users(id)
);
create table service_referral_rewards (
    id int auto_increment primary key,
    referral_id int not null,
    reward_amount decimal(10,2) not null,
    reward_date datetime default current_timestamp,
    status enum('pending','credited','failed') default 'pending',
    foreign key (referral_id) references service_referrals(id)
);
create table service_promotions_history (
    id int auto_increment primary key,
    promotion_id int not null,
    user_id int not null,
    redeemed_at datetime default current_timestamp,
    foreign key (promotion_id) references service_promotions(id),
    foreign key (user_id) references users(id)
);
create table service_custom_fields (
    id int auto_increment primary key,
    service_id int not null,
    field_name varchar(100) not null,
    field_type enum('text','number','date','select') not null,
    field_value text,
    created_at datetime default current_timestamp,
    foreign key (service_id) references services(id)
);
create table service_custom_field_options (
    id int auto_increment primary key,
    custom_field_id int not null,
    option_value varchar(100) not null,
    created_at datetime default current_timestamp,
    foreign key (custom_field_id) references service_custom_fields(id)
);
create table service_custom_field_responses (
    id int auto_increment primary key,
    booking_id int not null,
    custom_field_id int not null,
    response_value text,
    created_at datetime default current_timestamp,
    foreign key (booking_id) references bookings(id),
    foreign key (custom_field_id) references service_custom_fields(id)
);
create table service_custom_field_responses_history (
    id int auto_increment primary key,
    response_id int not null,
    changed_value text,
    changed_at datetime default current_timestamp,
    foreign key (response_id) references service_custom_field_responses(id)
);
create table service_custom_field_responses_logs (
    id int auto_increment primary key,
    response_id int not null,
    action enum('created','updated','deleted') not null,
    action_by int not null,
    action_at datetime default current_timestamp,
    foreign key (response_id) references service_custom_field_responses(id),
    foreign key (action_by) references users(id)
);

create table service_custom_field_responses_attachments (
    id int auto_increment primary key,
    response_id int not null,
    file_url varchar(255) not null,
    file_type varchar(50),
    created_at datetime default current_timestamp,
    foreign key (response_id) references service_custom_field_responses(id)
);

create table support_tickets (
    id int auto_increment primary key,
    user_id int not null,
    subject varchar(255) not null,
    message text not null,
    status enum('open','in_progress','resolved','closed') default 'open',
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp,
    foreign key (user_id) references users(id)
);
create table support_ticket_messages (
    id int auto_increment primary key,
    ticket_id int not null,
    sender_id int not null,
    message text not null,
    sent_at datetime default current_timestamp,
    is_read boolean default false,
    foreign key (ticket_id) references support_tickets(id),
    foreign key (sender_id) references users(id)
);
create table audit_logs (
    id int auto_increment primary key,
    user_id int,
    table_name varchar(100),
    record_id int,
    action enum('insert','update','delete'),
    changes text,
    timestamp datetime default current_timestamp,
    foreign key (user_id) references users(id)
);
create table provider_documents (
    id int auto_increment primary key,
    provider_id int not null,
    document_type varchar(100),
    document_url varchar(255),
    status enum('pending','approved','rejected') default 'pending',
    uploaded_at datetime default current_timestamp,
    foreign key (provider_id) references providers(id)
);
create table marketing_campaigns (
    id int auto_increment primary key,
    title varchar(100),
    content text,
    target_type enum('all','city','category','user'),
    target_value varchar(100),
    banner_image varchar(255),
    start_date datetime,
    end_date datetime,
    created_at datetime default current_timestamp
);
create table cms_pages (
    id int auto_increment primary key,
    slug varchar(100) not null unique,         -- e.g., 'home', 'about', 'terms'
    title varchar(255) not null,
    content longtext,                          -- HTML or rich content
    status enum('draft','published') default 'published',
    meta_title varchar(255),
    meta_description text,
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp
);
create table cms_sections (
    id int auto_increment primary key,
    page_slug varchar(100) not null,             -- e.g., 'home'
    section_key varchar(100) not null,           -- e.g., 'hero', 'why_us', 'testimonials'
    title varchar(255),
    content longtext,
    image_url varchar(255),
    position int default 0,
    status enum('active','inactive') default 'active',
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp
);
create table cms_section_blocks (
    id int auto_increment primary key,
    section_id int not null,
    block_type enum('text','image','video','html') not null,
    content longtext,
    position int default 0,
    created_at datetime default current_timestamp,
    updated_at datetime default current_timestamp on update current_timestamp,
    foreign key (section_id) references cms_sections(id)
);
create table cms_media (
    id int auto_increment primary key,
    type enum('image','video','file') not null,
    label varchar(100),
    file_url varchar(255) not null,
    uploaded_at datetime default current_timestamp
);
create table cms_media_categories (
    id int auto_increment primary key,
    name varchar(100) not null,
    description text,
    created_at datetime default current_timestamp
);
create table cms_media_category_assignments (
    id int auto_increment primary key,
    media_id int not null,
    category_id int not null,
    created_at datetime default current_timestamp,
    foreign key (media_id) references cms_media(id),
    foreign key (category_id) references cms_media_categories(id)
);
