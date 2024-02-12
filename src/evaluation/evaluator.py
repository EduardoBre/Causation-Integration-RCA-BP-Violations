from bert import encode_text, get_cosine_similarity

# Define Evaluation Thresholds
# F = fit, PF = partially fit, NF = not fit.

# activity-score thresholds
ACTIVITY_N_SCORE_F = 0.8
ACTIVITY_N_SCORE_PF = 0.6

# activities-relationship-score threshold
ACTIVITIES_RELATIONSHIP_SCORE = 0.8

# condition_feature_score thresholds
FEATURE_N_SCORE_F = 0.8
FEATURE_N_SCORE_PF = 0.60
VALUE_TEXTUAL_FEATURE_N_SCORE_F = 0.8
REL_FEATURE_N_SCORE_F = 1


def eval_activity_score(got_n: str, got_n1: str, ex_n: str, ex_n1: str) -> float | int:
    """
    Evaluates the activity-score.
    :param got_n: First activity (activity_n).
    :param got_n1: Second activity (activity_n+1).
    :param ex_n: Expected First activity (activity_n).
    :param ex_n1: Expected Second activity (activity_n+1).
    :return: Thesis evaluation of activity-score formula.
    """
    e_n = eval_cosine_similarity(got_n, ex_n)
    e_n1 = eval_cosine_similarity(got_n1, ex_n1)
    # Evaluate first activity
    if e_n > ACTIVITY_N_SCORE_F:
        score_n = 1
    elif e_n >= ACTIVITY_N_SCORE_PF:
        score_n = 0.5
    else:
        return 0
    # Evaluate second activity
    if e_n1 > ACTIVITY_N_SCORE_F:
        return score_n
    elif e_n1 >= ACTIVITY_N_SCORE_PF:
        return score_n * 0.5
    else:
        return 0


def eval_activities_relationship_score(got_rel: str, ex_rel: str) -> int:
    """
    Evaluates activities-relationship-score.
    :param got_rel: Mined relationship (as-is).
    :param ex_rel: Expected relationship (to-be).
    :return: Thesis evaluation of activities-relationship-score formula.
    """
    return 1 if got_rel.lower() == ex_rel.lower() else 0


def eval_feature_score(got_feature: str, ex_feature: str) -> float | int:
    e_feature = eval_cosine_similarity(got_feature, ex_feature)
    # Evaluate feature name
    if e_feature > FEATURE_N_SCORE_F:
        return 0.25
    elif e_feature >= FEATURE_N_SCORE_PF:
        return 0.125
    return 0


def eval_feature_relationship_score(got_rel: str, ex_rel: str) -> float | int:
    """
    Evaluates activities-relationship-score.
    :param got_rel: Mined relationship (as-is).
    :param ex_rel: Expected relationship (to-be).
    :return: Thesis evaluation of activities-relationship-score formula.
    """
    # no further feature relationships
    if not got_rel:
        return 0.25
    return 0.25 if got_rel.lower() == ex_rel.lower() else 0


def eval_feature_textual_value_score(got_val: str, ex_val: str) -> float | int:
    """
    Evaluates feature value score if the value is textually based.
    :param got_val: Mined value (as-is).
    :param ex_val: Expected value (to-be).
    :return: Thesis evaluation of feature-value-score formula.
    """
    # no further feature relationships
    if eval_cosine_similarity(got_val, ex_val) < VALUE_TEXTUAL_FEATURE_N_SCORE_F:
        return 0.0
    return 0.5


def eval_cosine_similarity(subject: str, object_: str, dec_rounding: int = 3):
    """
    Evaluates a subject (as-is) and object (to-be) string, encodes them using BERT model and calculates the cosine
    similarity.
    :param subject: The string (as-is) to be tested.
    :param object_: The string (to-be) to be used as a Gold-Standard.
    :param dec_rounding: The amount of decimals to round the similarity.
    :return: Float type similarity.
    """
    return round(get_cosine_similarity(encode_text(subject), encode_text(object_)), dec_rounding)


def eval_threshold(similarity: float, threshold: float) -> bool:
    """
    Returns true if similarity is above threshold, false otherwise.
    Helper function to keep code cleaner.
    """
    return similarity > threshold
