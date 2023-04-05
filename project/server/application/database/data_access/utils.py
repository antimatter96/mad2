def new_entities(klass, from_date, to_date):
  return klass.query.with_entities(klass.created_at)\
    .filter(klass.created_at > from_date)\
    .filter(klass.created_at <= to_date)\
    .count()
