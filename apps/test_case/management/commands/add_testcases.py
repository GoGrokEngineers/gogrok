from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
            {
            "input": {
                "root": {
                    "val": 3,
                    "left": {
                        "val": 1,
                        "left": None,
                        "right": {
                            "val": 2,
                            "left": None,
                            "right": None
                        }
                    },
                    "right": {
                        "val": 4,
                        "left": None,
                        "right": None
                    }
                },
                "k": 1
            },
            "output": 1,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 5,
                    "left": {
                        "val": 3,
                        "left": {
                            "val": 2,
                            "left": {
                                "val": 1,
                                "left": None,
                                "right": None
                            },
                            "right": None
                        },
                        "right": None
                    },
                    "right": {
                        "val": 6,
                        "left": None,
                        "right": None
                    }
                },
                "k": 3
            },
            "output": 3,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 7,
                    "left": {
                        "val": 5,
                        "left": {
                            "val": 3,
                            "left": {
                                "val": 2,
                                "left": None,
                                "right": None
                            },
                            "right": None
                        },
                        "right": {
                            "val": 6,
                            "left": None,
                            "right": None
                        }
                    },
                    "right": {
                        "val": 9,
                        "left": {
                            "val": 8,
                            "left": None,
                            "right": None
                        },
                        "right": None
                    }
                },
                "k": 4
            },
            "output": 5,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 1,
                    "left": None,
                    "right": {
                        "val": 2,
                        "left": None,
                        "right": {
                            "val": 3,
                            "left": None,
                            "right": None
                        }
                    }
                },
                "k": 2
            },
            "output": 2,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 10,
                    "left": {
                        "val": 5,
                        "left": {
                            "val": 3,
                            "left": {
                                "val": 2,
                                "left": None,
                                "right": None
                            },
                            "right": None
                        },
                        "right": {
                            "val": 7,
                            "left": {
                                "val": 6,
                                "left": None,
                                "right": None
                            },
                            "right": None
                        }
                    },
                    "right": {
                        "val": 15,
                        "left": {
                            "val": 13,
                            "left": None,
                            "right": {
                                "val": 14,
                                "left": None,
                                "right": None
                            }
                        },
                        "right": {
                            "val": 20,
                            "left": None,
                            "right": None
                        }
                    }
                },
                "k": 6
            },
            "output": 10,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 8,
                    "left": {
                        "val": 5,
                        "left": {
                            "val": 2,
                            "left": None,
                            "right": None
                        },
                        "right": {
                            "val": 6,
                            "left": None,
                            "right": None
                        }
                    },
                    "right": {
                        "val": 10,
                        "left": {
                            "val": 9,
                            "left": None,
                            "right": None
                        },
                        "right": None
                    }
                },
                "k": 2
            },
            "output": 6,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 20,
                    "left": {
                        "val": 10,
                        "left": {
                            "val": 5,
                            "left": {
                                "val": 3,
                                "left": None,
                                "right": None
                            },
                            "right": None
                        },
                        "right": {
                            "val": 15,
                            "left": None,
                            "right": None
                        }
                    },
                    "right": {
                        "val": 30,
                        "left": {
                            "val": 25,
                            "left": None,
                            "right": None
                        },
                        "right": {
                            "val": 35,
                            "left": None,
                            "right": None
                        }
                    }
                },
                "k": 5
            },
            "output": 15,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 12,
                    "left": {
                        "val": 7,
                        "left": {
                            "val": 5,
                            "left": None,
                            "right": None
                        },
                        "right": {
                            "val": 10,
                            "left": None,
                            "right": None
                        }
                    },
                    "right": {
                        "val": 15,
                        "left": {
                            "val": 14,
                            "left": None,
                            "right": None
                        },
                        "right": {
                            "val": 18,
                            "left": None,
                            "right": None
                        }
                    }
                },
                "k": 4
            },
            "output": 12,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "root": {
                    "val": 50,
                    "left": {
                        "val": 30,
                        "left": {
                            "val": 20,
                            "left": None,
                            "right": None
                        },
                        "right": {
                            "val": 40,
                            "left": None,
                            "right": None
                        }
                    },
                    "right": {
                        "val": 70,
                        "left": {
                            "val": 60,
                            "left": None,
                            "right": None
                        },
                        "right": {
                            "val": 80,
                            "left": None,
                            "right": None
                        }
                    }
                },
                "k": 7
            },
            "output": 70,
            "input_type": {
                "root": "TreeNode",
                "k": "int"
            },
            "output_type": {
                "result": "int"
            }
        }
		]
        

        task = Task.objects.get(title="Kth Smallest Element in a BST")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )