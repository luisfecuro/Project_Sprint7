# Librerias
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

df = pd.read_csv("vehicles_us.csv", sep=",")

df['is_4wd'] = df['is_4wd'].fillna(0)
df['is_4wd'] = df['is_4wd'].astype(bool)

df['paint_color'] = df['paint_color'].fillna('unknown')
df['cylinders'] = df['cylinders'].fillna('unknown')
df['brand'] = df['model'].str.split().str[0]
df['odometer'] = df['odometer'].fillna('unknown')
df['model_year'] = df['model_year'].fillna('unknown')
