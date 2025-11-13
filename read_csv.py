# -*- coding: utf-8 -*-

"""
قارئ البيانات الحقيقية لنظام الأحكام القانونية العربية
يقرأ ملف CSV ويحوله إلى قاعدة بيانات حقيقية
"""

import csv
import sys
import os
from datetime import datetime
import re

def read_csv_data():
    """قراءة بيانات CSV"""
    try:
        # قراءة الملف المرفوع
        with open('arabicljptraindata.csv', 'r', encoding='utf-8') as file:
            content = file.read()
            print("تم العثور على الملف!")
            print(f"حجم الملف: {len(content)} حرف")
            print(f"أول 500 حرف من الملف:")
            print(content[:500])
            return content
    except FileNotFoundError:
        print("لم يتم العثور على الملف. يرجى التأكد من وجود arabicljptraindata.csv في المجلد الحالي")
        return None
    except Exception as e:
        print(f"خطأ في قراءة الملف: {str(e)}")
        return None

if __name__ == "__main__":
    print("🔍 جاري البحث عن ملف البيانات...")
    data = read_csv_data()
    
    if data:
        print("\n✅ تم قراءة الملف بنجاح!")
    else:
        print("\n❌ فشل في قراءة الملف")
