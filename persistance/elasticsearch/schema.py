youtube_user_index= {
            "properties": {
                "active?": {
                "type": "boolean"
                },
                "category-id": {
                "type": "string",
                "index": "not_analyzed"
                },
                "channel": {
                "properties": {
                    "active?": {
                    "type": "boolean"
                    },
                    "auto-generated?": {
                    "type": "boolean",
                    "index": "no"
                    },
                    "banner-hd-image-url": {
                    "type": "string",
                    "index": "no"
                    },
                    "banner-image-url": {
                    "type": "string",
                    "index": "no"
                    },
                    "channel-attributes": {
                    "properties": {
                        "account-type": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                        "gender": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                        "race": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                        "religion": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                        "primary-language": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                        "education": {
                        "type": "string",
                        "index": "not_analyzed"
                        },
                        "date-of-birth-min": {
                        "type": "date",
                        "format": "dateOptionalTime"
                        },
                        "date-of-birth-max": {
                        "type": "date",
                        "format": "dateOptionalTime"
                        }
                    }
                    },
                    "channel-stats": {
                    "properties": {
                        "average-comments-per-video": {
                        "type": "double"
                        },
                        "average-dislikes-per-video": {
                        "type": "double"
                        },
                        "average-engagements-per-video": {
                        "type": "double"
                        },
                        "average-likes-per-video": {
                        "type": "double"
                        },
                        "average-video-duration-in-seconds": {
                        "type": "double"
                        },
                        "average-videos-per-day": {
                        "type": "double"
                        },
                        "average-views-per-video": {
                        "type": "double"
                        },
                        "flagged-video-count": {
                        "type": "long"
                        },
                        "flagged-video-percentage": {
                        "type": "double"
                        },
                        "hashoff-score": {
                        "type": "double"
                        },
                        "influencer?": {
                        "type": "boolean"
                        },
                        "last-processed-date": {
                        "type": "date",
                        "format": "dateOptionalTime",
                        "index": "no"
                        },
                        "last-retrieved-date": {
                        "type": "date",
                        "format": "dateOptionalTime",
                        "index": "no"
                        },
                        "latest-processed-video-id": {
                        "type": "string",
                        "index": "no"
                        },
                        "like-dislike-ratio": {
                        "type": "double"
                        },
                        "oldest-processed-video-id": {
                        "type": "string",
                        "index": "no"
                        },
                        "processed-entire-history": {
                        "type": "boolean"
                        },
                        "processed-video-count": {
                        "type": "long",
                        "index": "no"
                        },
                        "subscriber-video-ratio": {
                        "type": "double"
                        },
                        "tags-in-videos": {
                        "type": "string"
                        }
                    }
                    },
                    "comment-count": {
                    "type": "long"
                    },
                    "country": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "create-date": {
                    "type": "date",
                    "format": "dateOptionalTime"
                    },
                    "default-thumbnail-url": {
                    "type": "string",
                    "index": "no"
                    },
                    "description": {
                    "type": "string"
                    },
                    "etag": {
                    "type": "string",
                    "index": "no"
                    },
                    "favorites-channel-id": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "google-plus-user-id": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "hidden-subscriber-count?": {
                    "type": "boolean"
                    },
                    "high-thumbnail-url": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "id": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "keywords": {
                    "type": "string"
                    },
                    "likes-channel-id": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "linked?": {
                    "type": "boolean"
                    },
                    "medium-thumbnail-url": {
                    "type": "string",
                    "index": "no"
                    },
                    "privacy-status": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "profile-color": {
                    "type": "string",
                    "index": "no"
                    },
                    "subscriber-count": {
                    "type": "long"
                    },
                    "title": {
                    "type": "string"
                    },
                    "topic-ids": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "uploads-channel-id": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "video-count": {
                    "type": "long"
                    },
                    "view-count": {
                    "type": "long"
                    },
                    "watch-history-channel-id": {
                    "type": "string",
                    "index": "not_analyzed"
                    },
                    "watch-later-channel-id": {
                    "type": "string",
                    "index": "not_analyzed"
                    }
                }
                },
                "channel-id": {
                "type": "string",
                "index": "not_analyzed"
                },
                "channel-title": {
                "type": "string"
                },
                "comment-count": {
                "type": "long"
                },
                "description": {
                "type": "string"
                },
                "dislike-count": {
                "type": "long"
                },
                "duration-in-seconds": {
                "type": "long"
                },
                "embed-html": {
                "type": "string",
                "index": "no"
                },
                "embeddable?": {
                "type": "boolean"
                },
                "etag": {
                "type": "string",
                "index": "no"
                },
                "like-count": {
                "type": "long"
                },
                "live-broadcast-content": {
                "type": "string"
                },
                "public-stats-viewable?": {
                "type": "boolean"
                },
                "published-date": {
                "type": "date",
                "format": "dateOptionalTime"
                },
                "relevant-topic-ids": {
                "type": "string",
                "index": "not_analyzed"
                },
                "tags": {
                "type": "string"
                },
                "thumbnails": {
                "properties": {
                    "default": {
                    "properties": {
                        "height": {
                        "type": "long",
                        "index": "no"
                        },
                        "type": {
                        "type": "string",
                        "index": "no"
                        },
                        "url": {
                        "type": "string",
                        "index": "no"
                        },
                        "width": {
                        "type": "long",
                        "index": "no"
                        }
                    }
                    },
                    "high": {
                    "properties": {
                        "height": {
                        "type": "long",
                        "index": "no"
                        },
                        "type": {
                        "type": "string",
                        "index": "no"
                        },
                        "url": {
                        "type": "string",
                        "index": "no"
                        },
                        "width": {
                        "type": "long",
                        "index": "no"
                        }
                    }
                    },
                    "maxres": {
                    "properties": {
                        "height": {
                        "type": "long",
                        "index": "no"
                        },
                        "type": {
                        "type": "string",
                        "index": "no"
                        },
                        "url": {
                        "type": "string",
                        "index": "no"
                        },
                        "width": {
                        "type": "long",
                        "index": "no"
                        }
                    }
                    },
                    "medium": {
                    "properties": {
                        "height": {
                        "type": "long",
                        "index": "no"
                        },
                        "type": {
                        "type": "string",
                        "index": "no"
                        },
                        "url": {
                        "type": "string",
                        "index": "no"
                        },
                        "width": {
                        "type": "long",
                        "index": "no"
                        }
                    }
                    },
                    "standard": {
                    "properties": {
                        "height": {
                        "type": "long",
                        "index": "no"
                        },
                        "type": {
                        "type": "string",
                        "index": "no"
                        },
                        "url": {
                        "type": "string",
                        "index": "no"
                        },
                        "width": {
                        "type": "long",
                        "index": "no"
                        }
                    }
                    }
                }
                },
                "title": {
                "type": "string"
                },
                "topic-ids": {
                "type": "string",
                "index": "not_analyzed"
                },
                "view-count": {
                "type": "long"
                }
                }
                }
#   "order": 1,
#   "settings": {
#     "number_of_replicas": 2,
#     "number_of_shards": 1
#   },
#   "template": "youtube-search-*"