module_context = {
    "file_handling": {
        "description": "Gère toutes les opérations liées à la gestion et à la manipulation des fichiers.",
        "modules": {
            "extract": {
                "functions": {
                    "handle_text_extraction": {
                        "description": "Extrait le texte situé dans un fichier sous format PDF, Word ou TXT.",
                        "parameters": ["file_path"],
                        "output": "text"
                    }
                }
            }, 
            "open": {
                "functions": {
                    "open_file": {
                        "description": "Ouvre un fichier dont le chemin est spécifié.",
                        "parameters": ["file_path"],
                        "output": "open a file"
                    }
                }
            },
            "search": {
                "functions": {
                    "handle_file_search": {
                        "description": "Recherche dans l'explorateur les fichiers correspondant à une requête donnée.",
                        "parameters": ["name", "type"],
                        "output": "list of possible files"
                    }
                }
            }
        }
    },

    "system_control": {
        "description": "Gère les paramètres système comme la luminosité, le son, le microphone ainsi que l'état d'alimentation.",
        "modules": {
            "brightness": {
                "functions": {
                    "handle_brightness_command": {
                        "description": "Ajuste la luminosité de l'écran.",
                        "parameters": ["brightness_level" or "brightness_adjust"],
                        "output": "Change la luminosité de l'écran"
                    }
                }
            },
            "microphone": {
                "functions": {
                    "handle_microphone_command": {
                        "description": "Active ou désactive le microphone.",
                        "parameters": ["microphone_action"],
                        "output": "Allume ou éteint le microphone"
                    }
                }
            },
            "power": {
                "functions": {
                    "handle_power_command": {
                        "description": "Éteint, redémarre ou met en veille l'appareil.",
                        "parameters": ["power_action"],
                        "output": "Change l'état de l'appareil"
                    }
                }
            },
            "sound": {
                "functions": {
                    "handle_sound_command": {
                        "description": "Règle le niveau du son de l'appareil.",
                        "parameters": ["sound_level" or "sound_adjust"],
                        "output": "Change le niveau de son de l'appareil"
                    }
                }
            }
        }
    },

    "browser": {
        "description": "Gère les activités de navigation, comme les recherches web ou l'accès à des URLs spécifiques.",
        "modules": {
            "favoris": {
                "functions": {
                    "open_favorite_page": {
                        "description": "Ouvre un onglet enregistré dans les favoris du navigateur.",
                        "parameters": ["bookmark_name"],
                        "output": "Ouvre une page favorite"
                    }
                }
            },
            "search": {
                "functions": {
                    "perform_web_search": {
                        "description": "Effectue une recherche sur le navigateur par défaut.",
                        "parameters": ["search_query"],
                        "output": "Résultats de recherche web"
                    }
                }
            }
        }
    },

    "outside": {
        "description": "Interagit avec des API externes ou des modèles d'IA pour exécuter des actions comme résumer du texte, écrire, corriger ou répondre à des questions complexes.",
        "modules": {
            "question": {
                "functions": {
                    "handle_question_command": {
                        "description": "Pose une question à un modèle extérieur.",
                        "parameters": ["user_input", "model_endpoint"],
                        "output": "Réponse à la question"
                    }
                }
            },
            "resume": {
                "functions": {
                    "handle_resume_command": {
                        "description": "Résume un texte via un modèle extérieur.",
                        "parameters": ["user_input", "model_endpoint"],
                        "output": "Résumé du texte"
                    }
                }
            },
            "suggest": {
                "functions": {
                    "handle_suggest_command": {
                        "description": "Fait appel à un modèle extérieur pour suggérer des idées à partir d'un texte donné.",
                        "parameters": ["user_input", "model_endpoint"],
                        "output": "Suggestions générées"
                    }
                }
            },
            "write": {
                "functions": {
                    "handle_write_command": {
                        "description": "Utilise un modèle extérieur pour écrire un texte à partir des informations fournies.",
                        "parameters": ["user_input", "model_endpoint"],
                        "output": "Texte généré"
                    }
                }
            }
        }
    },
    
    "applications": {
        "description": "Intéragit avec les applications/programmes installés sur l'appareil",
        "modules": {
            "open": {
                "functions": {
                    "open_application": {
                        "description": "Trouve une application puis l'ouvre",
                        "parameters": ["app_name"],
                        "output": "Application ouverte"
                    }
                }
            }
        }
    }
}


### Tenter de rendre le contexte dynamique avec une indication de "Or any words that is corresponding/probable to be found in this context at a probability of 80%", peut_être inclure cette notion de "dynamique" dans assistant.py directement en géénralisant la notion "dynamique"
