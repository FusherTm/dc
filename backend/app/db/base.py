# app/db/base.py
from sqlalchemy.orm import declarative_base

# 1) Önce Base'i tanımla (modül import zincirinden önce hazır olsun)
Base = declarative_base()

# 2) Sonra modelleri yan-etki için içe aktar (tablolar Base.metadata'ya kaydolur)
# Bu import, tek tek sınıf çekmez; sadece tabloların deklarasyonunun çalışması için.
import app.models  # noqa: F401  # pylint: disable=unused-import
