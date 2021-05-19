#todo sql table definites and model declations

# coding: utf-8
from sqlalchemy import Column, Enum, Float, ForeignKey, ForeignKeyConstraint, Index, LargeBinary, String, TIMESTAMP, Table, Text, text, DateTime, func
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, SMALLINT, TINYBLOB, TINYTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import join

from app.base import Base

# Base = declarative_base()
# metadata = Base.metadata


class AnalysisRule(Base):
    __tablename__ = 'analysis_rules'

    id = Column(INTEGER(11), primary_key=True)
    min_audience_size = Column(INTEGER(11))
    min_avg_engagements = Column(INTEGER(11))
    min_audience_ratio = Column(Float(asdecimal=True))
    max_posts_per_day = Column(INTEGER(11))
    creator_refresh_seconds = Column(INTEGER(11))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Company(Base):
    __tablename__ = 'company'

    id = Column(INTEGER(11), primary_key=True)
    added_by_user_id = Column(ForeignKey('user.id'), index=True)
    name = Column(String(100), nullable=False, unique=True)
    square_image_url = Column(String(2048))
    facebook_enabled = Column(Enum('T', 'F'), server_default=text("'T'"))
    instagram_enabled = Column(Enum('T', 'F'), server_default=text("'T'"))
    twitter_enabled = Column(Enum('T', 'F'), server_default=text("'T'"))
    youtube_enabled = Column(Enum('T', 'F'), server_default=text("'T'"))
    seat_limit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    seats_used = Column(INTEGER(11), server_default=text("'0'"))
    campaign_limit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    campaigns_used = Column(INTEGER(11), server_default=text("'0'"))
    facebook_limit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    facebook_searches_used = Column(INTEGER(11), server_default=text("'0'"))
    instagram_limit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_searches_used = Column(INTEGER(11), server_default=text("'0'"))
    twitter_limit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_searches_used = Column(INTEGER(11), server_default=text("'0'"))
    youtube_limit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_searches_used = Column(INTEGER(11), server_default=text("'0'"))
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    added_by_user = relationship('User', primaryjoin='Company.added_by_user_id == User.id')


# t_database_migrations = Table(
#     'database_migrations', metadata,
#     Column('id', String(255, 'utf8mb4_unicode_ci')),
#     Column('created_at', String(32, 'utf8mb4_unicode_ci'))
# )


class EmailAddres(Base):
    __tablename__ = 'email_address'

    id = Column(INTEGER(11), primary_key=True)
    email_address = Column(String(180), nullable=False, unique=True)
    transactional_opt_out = Column(Enum('T', 'F'), nullable=False, server_default=text("'F'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class MarketplaceWaitlistEntry(EmailAddres):
    __tablename__ = 'marketplace_waitlist_entry'

    email_address_id = Column(ForeignKey('email_address.id'), primary_key=True)
    joined_newsletter = Column(Enum('T', 'F'), server_default=text("'F'"))
    ip_address = Column(String(256))
    join_invitation_batch_id = Column(ForeignKey('marketplace_join_invitation_batch.id'), index=True)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    join_invitation_batch = relationship('MarketplaceJoinInvitationBatch')


class NewsletterInvitation(EmailAddres):
    __tablename__ = 'newsletter_invitation'

    email_address_id = Column(ForeignKey('email_address.id'), primary_key=True)
    created_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    email_status = Column(Enum('pending', 'sent', 'viewed', 'error'), nullable=False, server_default=text("'pending'"))
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128))
    opening_message = Column(TINYTEXT, nullable=False)
    signed_by = Column(String(128), nullable=False)
    network = Column(Enum('facebook', 'instagram', 'twitter', 'youtube'), nullable=False)
    network_creator_id = Column(String(128), nullable=False)
    acceptance_status = Column(Enum('pending', 'accepted', 'declined'), nullable=False, server_default=text("'pending'"))
    email_view_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    website_view_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    emailed_date = Column(TIMESTAMP)
    responded_date = Column(TIMESTAMP)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    created_by_user = relationship('User')


class MarketplaceInvitation(EmailAddres):
    __tablename__ = 'marketplace_invitation'

    email_address_id = Column(ForeignKey('email_address.id'), primary_key=True)
    marketplace_invitation_batch_id = Column(ForeignKey('marketplace_invitation_batch.id'), index=True)
    created_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    email_status = Column(Enum('pending', 'scheduled', 'sent', 'viewed', 'error'), nullable=False, server_default=text("'pending'"))
    first_name = Column(String(128))
    last_name = Column(String(128))
    network = Column(Enum('facebook', 'instagram', 'twitter', 'youtube'))
    network_creator_id = Column(String(128))
    acceptance_status = Column(Enum('pending', 'accepted', 'declined'), nullable=False, server_default=text("'pending'"))
    email_view_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    website_view_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    emailed_date = Column(TIMESTAMP)
    responded_date = Column(TIMESTAMP)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    created_by_user = relationship('User')
    marketplace_invitation_batch = relationship('MarketplaceInvitationBatch')


class InstagramAndroidClient(Base):
    __tablename__ = 'instagram_android_client'

    id = Column(BIGINT(20), primary_key=True)
    encrypted_client_edn = Column(LargeBinary, nullable=False)
    status = Column(Enum('active', 'inactive'), nullable=False, server_default=text("'active'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class InstagramToken(Base):
    __tablename__ = 'instagram_token'

    id = Column(INTEGER(11), primary_key=True)
    instagram_user_id = Column(BIGINT(20), nullable=False)
    username = Column(String(255), nullable=False)
    encrypted_access_token = Column(TINYBLOB, nullable=False)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class MarketplaceJoinInvitationBatch(Base):
    __tablename__ = 'marketplace_join_invitation_batch'

    id = Column(INTEGER(11), primary_key=True)
    created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    subject = Column(String(1024))


class MonitoredHashtag(Base):
    __tablename__ = 'monitored_hashtag'

    hashtag = Column(String(80), primary_key=True)
    is_monitored_on_instagram = Column(Enum('T', 'F'), nullable=False, server_default=text("'F'"))
    is_monitored_on_twitter = Column(Enum('T', 'F'), nullable=False, server_default=text("'F'"))
    is_monitored_on_youtube = Column(Enum('T', 'F'), nullable=False, server_default=text("'F'"))
    instagram_last_processed_start_date = Column(TIMESTAMP)
    instagram_last_processed_end_date = Column(TIMESTAMP)
    instagram_minimum_engagements_filter = Column(INTEGER(11), nullable=False, server_default=text("'25'"))
    youtube_last_processed_start_date = Column(TIMESTAMP)
    youtube_last_processed_end_date = Column(TIMESTAMP)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))


class ProspectDenialReason(Base):
    __tablename__ = 'prospect_denial_reason'

    id = Column(INTEGER(11), primary_key=True)
    reason = Column(String(255), nullable=False)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Proxy(Base):
    __tablename__ = 'proxy'

    id = Column(INTEGER(11), primary_key=True)
    ip_address = Column(String(45), nullable=False)
    port = Column(INTEGER(11))
    username = Column(String(255))
    encrypted_password = Column(LargeBinary)
    tags = Column(Text)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class ScrappingAccount(Base):
    __tablename__ = 'scrapping_account'

    id = Column(INTEGER(11), primary_key=True)
    social_network = Column(String(32), nullable=False)
    name = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    encrypted_password = Column(TINYBLOB, nullable=False)
    preferred_proxy_url = Column(String(255))
    cookie_header = Column(Text)
    guid = Column(String(128))
    csrf_token = Column(String(128))
    status = Column(String(32), nullable=False, server_default=text("'unauthenticated'"))
    last_login = Column(TIMESTAMP)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class SocialNetwork(Base):
    __tablename__ = 'social_network'

    id = Column(SMALLINT(6), primary_key=True)
    name = Column(String(64), nullable=False)


class SocialNetworkUserRemovalReason(Base):
    __tablename__ = 'social_network_user_removal_reason'

    id = Column(INTEGER(11), primary_key=True)
    reason = Column(String(512), nullable=False)
    is_active = Column(Enum('Y', 'N'), nullable=False, server_default=text("'Y'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class StopWord(Base):
    __tablename__ = 'stop_words'

    id = Column(INTEGER(11), primary_key=True)
    word = Column(String(128), nullable=False)


class TwitterApplication(Base):
    __tablename__ = 'twitter_application'

    id = Column(INTEGER(11), primary_key=True)
    application_name = Column(String(128), nullable=False)
    consumer_key = Column(String(255), nullable=False)
    encrypted_consumer_secret = Column(TINYBLOB, nullable=False)
    access_token = Column(String(255), nullable=False)
    encrypted_access_token_secret = Column(TINYBLOB, nullable=False)
    is_used_for_streaming = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class TwitterToken(Base):
    __tablename__ = 'twitter_token'

    id = Column(INTEGER(11), primary_key=True)
    twitter_user_id = Column(BIGINT(20), nullable=False)
    screen_name = Column(String(64), nullable=False)
    consumer_key = Column(String(255), nullable=False)
    encrypted_consumer_secret = Column(TINYBLOB, nullable=False)
    access_token = Column(String(255), nullable=False)
    encrypted_access_token_secret = Column(TINYBLOB, nullable=False)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    company_id = Column(ForeignKey('company.id'), nullable=False, index=True)
    email_address = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(64), nullable=False)
    role = Column(Enum('super-user', 'hashoff-admin', 'company-admin', 'company-user'), nullable=False, server_default=text("'company-user'"))
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    company = relationship('Company', primaryjoin='User.company_id == Company.id')


class YoutubeToken(Base):
    __tablename__ = 'youtube_token'

    id = Column(INTEGER(11), primary_key=True)
    application_name = Column(String(255), nullable=False)
    encrypted_api_key = Column(TINYBLOB, nullable=False)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Campaign(Base):
    __tablename__ = 'campaign'

    id = Column(INTEGER(11), primary_key=True)
    company_id = Column(ForeignKey('company.id', ondelete='CASCADE'), nullable=False, index=True)
    created_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    end_date = Column(TIMESTAMP)
    facebook_enabled = Column(Enum('T', 'F'), nullable=False, server_default=text("'F'"))
    instagram_enabled = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    twitter_enabled = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    youtube_enabled = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    facebook_engagement_target = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_engagement_target = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_engagement_target = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_engagement_target = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    search_query = Column(Text)
    min_ff_ratio = Column(Float(asdecimal=True))
    max_ff_ratio = Column(Float(asdecimal=True))
    min_fp_ratio = Column(Float(asdecimal=True))
    max_fp_ratio = Column(Float(asdecimal=True))
    min_followers = Column(INTEGER(11))
    max_followers = Column(INTEGER(11))
    min_engagements = Column(INTEGER(11))
    max_engagements = Column(INTEGER(11))
    min_posts = Column(INTEGER(11))
    max_posts = Column(INTEGER(11))
    post_types = Column(String(255))
    account_type = Column(Enum('all', 'verified', 'unverified'), nullable=False, server_default=text("'unverified'"))
    account_types = Column(String(255), server_default=text("'unknown,individual'"))
    top_level_taxonomy = Column(String(255))
    second_level_taxonomy = Column(String(255))
    facebook_category = Column(String(255))
    search_window = Column(INTEGER(11))
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    total_facebook_posts = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_instagram_posts = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_twitter_posts = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_youtube_posts = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_facebook_influencers = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_instagram_influencers = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_twitter_influencers = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_youtube_influencers = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_denials = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_facebook_denials = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_instagram_denials = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_twitter_denials = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_youtube_denials = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_searches_executed = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_facebook_searches_executed = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_instagram_searches_executed = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_twitter_searches_executed = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_youtube_searches_executed = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_collection_searches = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_facebook_collection_searches = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_instagram_collection_searches = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_twitter_collection_searches = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_youtube_collection_searches = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_dislikes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_shares = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    facebook_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    facebook_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    facebook_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    facebook_reactions = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    facebook_shares = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    facebook_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    facebook_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    instagram_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    instagram_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    twitter_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_shares = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    twitter_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    youtube_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_dislikes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    youtube_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    status = Column(Enum('active', 'inactive', 'complete'), nullable=False, server_default=text("'active'"))
    total_influencers = Column(INTEGER(11), nullable=False, server_default=text("'0'"))

    company = relationship('Company')
    created_by_user = relationship('User')


class CampaignDeniedProspect(Base):
    __tablename__ = 'campaign_denied_prospect'
    __table_args__ = (
        Index('unq_campaign_denied_prospect_social_network_user', 'campaign_id', 'social_network', 'social_network_user_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    campaign_id = Column(INTEGER(11), nullable=False)
    social_network = Column(Enum('facebook', 'twitter', 'instagram', 'youtube'), nullable=False)
    social_network_user_id = Column(String(32), nullable=False)
    post_id = Column(String(155))
    denied_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    prospect_denial_reason_id = Column(ForeignKey('prospect_denial_reason.id'), index=True)
    denial_notes = Column(TINYTEXT)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    denied_by_user = relationship('User')
    prospect_denial_reason = relationship('ProspectDenialReason')


class CollectionSearchGroup(Base):
    __tablename__ = 'collection_search_group'

    id = Column(INTEGER(11), primary_key=True)
    description = Column(Text)
    grouping_type = Column(String(64), nullable=False)
    base_query = Column(Text, nullable=False)
    added_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    added_by_user = relationship('User')


class CompanyInstagramAccount(Base):
    __tablename__ = 'company_instagram_account'
    __table_args__ = (
        Index('unq_company_instagram_account_company_instagram_user_id', 'company_id', 'instagram_user_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    company_id = Column(ForeignKey('company.id', ondelete='CASCADE'), nullable=False, index=True)
    connected_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    instagram_user_id = Column(BIGINT(20), nullable=False)
    username = Column(String(64), nullable=False)
    full_name = Column(String(255))
    profile_picture = Column(String(255), nullable=False)
    encrypted_access_token = Column(TINYBLOB, nullable=False)
    is_valid = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    company = relationship('Company')
    connected_by_user = relationship('User')


class CompanyTwitterAccount(Base):
    __tablename__ = 'company_twitter_account'
    __table_args__ = (
        Index('unq_company_twitter_account_company_twitter_user_id', 'company_id', 'twitter_user_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    company_id = Column(ForeignKey('company.id', ondelete='CASCADE'), nullable=False, index=True)
    connected_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    twitter_user_id = Column(BIGINT(20), nullable=False)
    screen_name = Column(String(64), nullable=False)
    oauth_access_token = Column(String(255), nullable=False)
    encrypted_oauth_access_token_secret = Column(TINYBLOB, nullable=False)
    is_valid = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    company = relationship('Company')
    connected_by_user = relationship('User')


class InstagramUserClassificationEntry(Base):
    __tablename__ = 'instagram_user_classification_entry'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    created_by_user_id = Column(ForeignKey('user.id'), index=True)
    classification = Column(Enum('good', 'bad', 'unknown'), nullable=False, server_default=text("'unknown'"))
    account_type = Column(Enum('individual', 'business', 'aggregator', 'website', 'bot', 'pet'))
    language = Column(String(2))
    email_address = Column(String(256))
    first_name = Column(String(128))
    last_name = Column(String(128))
    error = Column(String(32))
    shortcuts_used = Column(String(128))
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    created_by_user = relationship('User')


class MarketplaceInvitationBatch(Base):
    __tablename__ = 'marketplace_invitation_batch'

    id = Column(INTEGER(11), primary_key=True)
    created_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    sendgrid_batch_id = Column(String(1024))
    batch_status = Column(Enum('pending', 'scheduled'), nullable=False)
    send_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    subject = Column(String(255), nullable=False)
    desired_batch_size = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    batch_size = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    sendgrid_template_id = Column(String(64))
    created_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    created_by_user = relationship('User')


class ProfileAttributeEntry(Base):
    __tablename__ = 'profile_attribute_entry'
    __table_args__ = (
        Index('idx_social_network_user', 'social_network_id', 'social_network_user_id'),
    )

    id = Column(BIGINT(20), primary_key=True)
    social_network_id = Column(ForeignKey('social_network.id'), nullable=False)
    social_network_user_id = Column(String(32), nullable=False)
    added_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    entry_type = Column(Enum('add', 'remove'), nullable=False)
    attribute_key = Column(String(30), nullable=False)
    attribute_value = Column(String(256), nullable=False)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    added_by_user = relationship('User')
    social_network = relationship('SocialNetwork')


class SocialNetworkUserRemoval(Base):
    __tablename__ = 'social_network_user_removal'

    id = Column(BIGINT(20), primary_key=True)
    social_network_id = Column(ForeignKey('social_network.id'), nullable=False, index=True)
    social_network_user_id = Column(String(30), nullable=False)
    removed_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    social_network_user_removal_reason_id = Column(ForeignKey('social_network_user_removal_reason.id'), index=True)
    removal_notes = Column(Text)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    removed_by_user = relationship('User')
    social_network = relationship('SocialNetwork')
    social_network_user_removal_reason = relationship('SocialNetworkUserRemovalReason')


class UserAuthToken(Base):
    __tablename__ = 'user_auth_token'

    token = Column(String(64), primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')


class CampaignAnalyticsSnapshot(Base):
    __tablename__ = 'campaign_analytics_snapshot'

    campaign_id = Column(ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    capture_date = Column(TIMESTAMP, primary_key=True, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    total_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_dislikes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_shares = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    total_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    twitter_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_shares = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    twitter_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    twitter_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    instagram_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    instagram_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    instagram_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    youtube_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_dislikes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    youtube_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    youtube_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    campaign = relationship('Campaign')


class CampaignHashtag(Base):
    __tablename__ = 'campaign_hashtag'

    campaign_id = Column(ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    hashtag = Column(String(64), primary_key=True, nullable=False)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    campaign = relationship('Campaign')


class CampaignInfluencer(Base):
    __tablename__ = 'campaign_influencer'
    __table_args__ = (
        Index('unq_campaign_influencer_social_network_user', 'campaign_id', 'social_network', 'social_network_user_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    campaign_id = Column(ForeignKey('campaign.id'), nullable=False)
    social_network = Column(Enum('facebook', 'twitter', 'instagram', 'youtube'), nullable=False)
    social_network_user_id = Column(String(32), nullable=False)
    post_id = Column(String(155))
    approved_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    acceptance_status = Column(Enum('accepted', 'declined', 'pending', 'not-applicable'), server_default=text("'pending'"))
    notes = Column(TINYTEXT)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    total_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    total_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    total_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_dislikes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_shares = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    sort_order = Column(Float(asdecimal=True))

    approved_by_user = relationship('User')
    campaign = relationship('Campaign')


class CampaignInfluencerImport(Base):
    __tablename__ = 'campaign_influencer_import'
    __table_args__ = (
        Index('unq_campaign_influencer_import_social_network_user', 'campaign_id', 'social_network', 'social_network_user_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    campaign_id = Column(ForeignKey('campaign.id'), nullable=False, index=True)
    social_network = Column(Enum('twitter', 'instagram', 'youtube'), nullable=False)
    social_network_user_id = Column(String(32), nullable=False)
    post_id = Column(String(155), nullable=False)
    added_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    import_status = Column(Enum('non-influencer', 'influencer', 'pending'), server_default=text("'pending'"))
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    added_by_user = relationship('User')
    campaign = relationship('Campaign')


class CampaignMessageTemplate(Base):
    __tablename__ = 'campaign_message_template'

    id = Column(INTEGER(11), primary_key=True)
    campaign_id = Column(ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False, index=True)
    created_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    message_template = Column(String(1024), nullable=False)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    campaign = relationship('Campaign')
    created_by_user = relationship('User')


class CollectionSearch(Base):
    __tablename__ = 'collection_search'

    id = Column(INTEGER(11), primary_key=True)
    collection_search_group_id = Column(ForeignKey('collection_search_group.id'), index=True)
    query = Column(Text, nullable=False)
    description = Column(Text)
    added_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    added_by_user = relationship('User')
    collection_search_group = relationship('CollectionSearchGroup')


class InstagramUserClassification(Base):
    __tablename__ = 'instagram_user_classification'

    user_id = Column(BIGINT(20), primary_key=True)
    classification_status = Column(Enum('unassigned', 'assigned', 'complete', 'error'), nullable=False, index=True, server_default=text("'unassigned'"))
    assigned_to_user_id = Column(ForeignKey('user.id'), index=True)
    marketplace_invitation_batch_id = Column(ForeignKey('marketplace_invitation_batch.id'), index=True)
    classification = Column(Enum('good', 'bad', 'unknown'), nullable=False, server_default=text("'unknown'"))
    account_type = Column(Enum('individual', 'business', 'aggregator', 'website', 'bot', 'pet'))
    language = Column(String(2))
    email_address = Column(String(256))
    first_name = Column(String(128))
    last_name = Column(String(128))
    error = Column(String(32))
    last_collection_date = Column(TIMESTAMP, nullable=False, index=True)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    assigned_to_user = relationship('User')
    marketplace_invitation_batch = relationship('MarketplaceInvitationBatch')


class CampaignInstagramContent(Base):
    __tablename__ = 'campaign_instagram_content'
    __table_args__ = (
        Index('unq_campaign_instagram_content_media', 'influencer_id', 'media_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    campaign_id = Column(ForeignKey('campaign.id'), nullable=False, index=True)
    influencer_id = Column(ForeignKey('campaign_influencer.id', ondelete='CASCADE'), nullable=False, index=True)
    added_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    instagram_user_id = Column(BIGINT(20), nullable=False)
    media_id = Column(String(50), nullable=False)
    media_link = Column(String(2048), nullable=False)
    thumbnail_url = Column(String(2048), nullable=False)
    caption_text = Column(Text)
    media_created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    added_by_user = relationship('User')
    campaign = relationship('Campaign')
    influencer = relationship('CampaignInfluencer')


class CampaignPostAnalyticsSnapshot(Base):
    __tablename__ = 'campaign_post_analytics_snapshot'

    id = Column(INTEGER(11), primary_key=True)
    campaign_id = Column(ForeignKey('campaign.id'), nullable=False, index=True)
    campaign_influencer_id = Column(ForeignKey('campaign_influencer.id', ondelete='CASCADE'), nullable=False, index=True)
    social_network_id = Column(ForeignKey('social_network.id'), nullable=False, index=True)
    social_network_user_id = Column(String(32), nullable=False)
    social_network_post_id = Column(String(64), nullable=False)
    total_engagements = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_likes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_dislikes = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_comments = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_shares = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_views = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    total_reach = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    total_impressions = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    campaign = relationship('Campaign')
    campaign_influencer = relationship('CampaignInfluencer')
    social_network = relationship('SocialNetwork')


class CampaignTwitterMessage(Base):
    __tablename__ = 'campaign_twitter_message'

    id = Column(INTEGER(11), primary_key=True)
    campaign_id = Column(ForeignKey('campaign.id'), nullable=False, index=True)
    created_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    company_twitter_account_id = Column(ForeignKey('company_twitter_account.id'), index=True)
    campaign_message_template_id = Column(ForeignKey('campaign_message_template.id'), index=True)
    influencer_id = Column(ForeignKey('campaign_influencer.id', ondelete='CASCADE'), index=True)
    twitter_user_id = Column(BIGINT(20), nullable=False)
    in_reply_to_status_id = Column(BIGINT(20))
    text = Column(String(1024), nullable=False)
    status_id = Column(BIGINT(20))
    status_created_date = Column(TIMESTAMP)
    error_code = Column(INTEGER(11))
    http_status = Column(INTEGER(11))
    error_date = Column(TIMESTAMP)
    created_date = Column(TIMESTAMP, nullable=False, server_default=func.now())
    modified_date = Column(TIMESTAMP, nullable=False, server_default=func.now())

    campaign = relationship('Campaign')
    campaign_message_template = relationship('CampaignMessageTemplate')
    company_twitter_account = relationship('CompanyTwitterAccount')
    created_by_user = relationship('User')
    influencer = relationship('CampaignInfluencer')


class CollectionSearchExecution(Base):
    __tablename__ = 'collection_search_execution'

    id = Column(BIGINT(20), primary_key=True)
    collection_search_id = Column(ForeignKey('collection_search.id', ondelete='CASCADE'), nullable=False, index=True)
    network_id = Column(ForeignKey('social_network.id', ondelete='CASCADE'), nullable=False, index=True)
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)
    entities_seen = Column(INTEGER(11), nullable=False)
    entities_analyzed = Column(INTEGER(11), nullable=False)

    collection_search = relationship('CollectionSearch')
    network = relationship('SocialNetwork')


class CollectionSearchSchedule(Base):
    __tablename__ = 'collection_search_schedule'

    collection_search_id = Column(ForeignKey('collection_search.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    network_id = Column(ForeignKey('social_network.id'), primary_key=True, nullable=False, index=True)
    analysis_rules_id = Column(ForeignKey('analysis_rules.id'), index=True)
    collection_frequency_in_hours = Column(INTEGER(11), nullable=False)
    last_scheduled_date = Column(TIMESTAMP, index=True)
    last_executed_date = Column(TIMESTAMP, index=True)
    added_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    is_active = Column(Enum('T', 'F'), nullable=False, server_default=text("'T'"))
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    added_by_user = relationship('User')
    analysis_rules = relationship('AnalysisRule')
    collection_search = relationship('CollectionSearch')
    network = relationship('SocialNetwork')


class CompanyCollectionSearchSchedule(Base):
    __tablename__ = 'company_collection_search_schedule'
    __table_args__ = (
        ForeignKeyConstraint(['collection_search_id', 'network_id'], ['collection_search_schedule.collection_search_id', 'collection_search_schedule.network_id']),
        Index('fk_ccss_collection_search_schedule', 'collection_search_id', 'network_id'),
        Index('unq_ccss_company_collection_search_network', 'company_id', 'network_id', 'collection_search_id', unique=True)
    )

    id = Column(INTEGER(11), primary_key=True)
    company_id = Column(ForeignKey('company.id'), nullable=False, index=True)
    campaign_id = Column(ForeignKey('campaign.id'), index=True)
    collection_search_id = Column(ForeignKey('collection_search.id'), nullable=False, index=True)
    network_id = Column(ForeignKey('social_network.id'), nullable=False, index=True)
    analysis_rules_id = Column(ForeignKey('analysis_rules.id'), index=True)
    added_by_user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    is_active = Column(Enum('T', 'F'), nullable=False)
    created_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    added_by_user = relationship('User')
    analysis_rules = relationship('AnalysisRule')
    campaign = relationship('Campaign')
    collection_search = relationship('CollectionSearchSchedule')
    collection_search1 = relationship('CollectionSearch')
    company = relationship('Company')
    network = relationship('SocialNetwork')
