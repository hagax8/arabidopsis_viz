import altair as alt
from altair.expr import datum, substring
from vega_datasets import data
from sys import argv
import pandas as pd
df = pd.read_csv(argv[1])

df = df.dropna(subset=['longitude', 'latitude'])

countries = alt.topo_feature(data.world_110m.url, 'countries')

selection = alt.selection_multi(fields=['admixed group'])

color = alt.condition(selection,
                      alt.Color('admixed group:N', legend=None),
                      alt.value('#EEEEEE'))

brush = alt.selection_interval()
hover = alt.selection(type='single',
                      fields=["accession"])

chart = alt.Chart(countries).mark_geoshape(
    fill='#CCCCCC',
    stroke='white',
    opacity=0.4
).properties(
    width=850,
    height=850
)

chart += alt.Chart(df).mark_circle(size=30, stroke="black", strokeWidth=0.3).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    color=color,
    size=alt.condition(~hover, alt.value(30), alt.value(300)),
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by']
).project(type="orthographic").add_selection(hover).transform_filter(selection).transform_filter(brush)

text = alt.Chart(df).mark_text(align='right').encode(
    alt.Text('name', type='nominal'),
    longitude='longitude:Q',
    latitude='latitude:Q',
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by'],
    opacity=alt.condition(~hover, alt.value(0), alt.value(1))
).transform_filter(selection).transform_filter(brush).transform_filter(hover)

chart += text
chart_GTM = alt.Chart(df).mark_circle(size=30, strokeWidth=0.4).encode(
    x=alt.X("GTM axis 1", axis=alt.Axis(
        ticks=False, labels=False, grid=False)),
    y=alt.Y("GTM axis 2", axis=alt.Axis(
        ticks=False, labels=False, grid=False)),
    color=color,
    size=alt.condition(~hover, alt.value(30), alt.value(300)),
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by']
).properties(
    width=250,
    height=250,
).add_selection(brush).add_selection(hover)

text = alt.Chart(df).mark_text(align='right').encode(
    alt.Text('name', type='nominal'),
    x=alt.X("GTM axis 1"),
    y=alt.Y("GTM axis 2"),
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by'],
    opacity=alt.condition(~hover, alt.value(0), alt.value(1))
).transform_filter(selection).transform_filter(hover)

chart_GTM += text

chart_tSNE = alt.Chart(df).mark_circle(size=30, strokeWidth=0.4).encode(
    x=alt.X("t-SNE axis 1", axis=alt.Axis(ticks=False, labels=False, grid=False)),
    y=alt.Y("t-SNE axis 2", axis=alt.Axis(ticks=False, labels=False, grid=False)),
    color=color,
    size=alt.condition(~hover, alt.value(30), alt.value(300)),
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by']
).properties(
    width=250,
    height=250,
).add_selection(brush).add_selection(hover)

text = alt.Chart(df).mark_text(align='right').encode(
    alt.Text('name', type='nominal'),
    x=alt.X("t-SNE axis 1", axis=alt.Axis(ticks=False, labels=False, grid=False)),
    y=alt.Y("t-SNE axis 2", axis=alt.Axis(ticks=False, labels=False, grid=False)),
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by'],
    opacity=alt.condition(~hover, alt.value(0), alt.value(1))
).transform_filter(selection).transform_filter(hover)

chart_tSNE += text

chart_PCA = alt.Chart(df).mark_circle(size=30, strokeWidth=0.4).encode(
    x=alt.X("Principal component 1", axis=alt.Axis(
        ticks=False, labels=False, grid=False)),
    y=alt.Y("Principal component 2", axis=alt.Axis(
        ticks=False, labels=False, grid=False)),
    color=color,
    size=alt.condition(~hover, alt.value(30), alt.value(300)),
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by']
).properties(
    width=250,
    height=250,
).add_selection(brush).add_selection(hover)

text = alt.Chart(df).mark_text(align='right').encode(
    alt.Text('name', type='nominal'),
    x=alt.X("Principal component 1", axis=alt.Axis(
        ticks=False, labels=False, grid=False)),
    y=alt.Y("Principal component 2", axis=alt.Axis(
        ticks=False, labels=False, grid=False)),
    tooltip=['accession', 'name', 'country', 'admixed group',
             'continent', 'country code', 'CS number',
             'latitude', 'longitude',
             'collector', 'site', 'seq by'],
    opacity=alt.condition(~hover, alt.value(0), alt.value(1))
).transform_filter(selection).transform_filter(hover)

chart_PCA += text

legend = alt.Chart().mark_rect().encode(
    y=alt.Y('admixed group:N', axis=alt.Axis(
        orient='left', title="Admixed group")),
    color=color
).add_selection(
    selection
).transform_filter(brush)

hcharts = alt.hconcat(chart_GTM, chart_tSNE, chart_PCA, data=df)
chart = alt.hconcat(legend, chart, data=df)
vcharts = alt.vconcat(hcharts, chart, data=df
                      )

vcharts.save(argv[2]+'.html')
