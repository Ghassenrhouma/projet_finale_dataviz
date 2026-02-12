import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from typing import Optional


def generate_plotly_visualization(df: pd.DataFrame, viz_type: str, x_col: Optional[str] = None, y_col: Optional[str] = None):
    """
    Generate a Plotly visualization with proper titles, axes, and legends.
    Follows visualization best practices: right chart type, good data-ink ratio, no chartjunk.

    Args:
        df (pd.DataFrame): Dataset.
        viz_type (str): Type of visualization.
        x_col (str, optional): X-axis column.
        y_col (str, optional): Y-axis column.

    Returns:
        plotly figure.
    """
    # Sample large datasets for performance
    if len(df) > 1000:
        df_sample = df.sample(min(1000, len(df)), random_state=42)
    else:
        df_sample = df

    try:
        if viz_type == 'bar':
            if x_col and y_col:
                # Aggregate if needed and limit categories
                if df_sample[x_col].nunique() > 20:
                    top_categories = df.groupby(x_col)[y_col].sum().nlargest(15).index
                    df_sample = df_sample[df_sample[x_col].isin(top_categories)]
                fig = px.bar(df_sample, x=x_col, y=y_col, 
                           title=f"{y_col.replace('_', ' ').title()} by {x_col.replace('_', ' ').title()}",
                           color_discrete_sequence=['#3498db'])  # Professional blue
                # Ensure colors persist
                fig.update_traces(marker_color='#3498db', marker_line_color='white', marker_line_width=0.5)
            elif x_col:
                # Count the values in x_col
                counts = df[x_col].value_counts().head(15).reset_index()
                counts.columns = [x_col, 'count']
                fig = px.bar(counts, x=x_col, y='count', 
                           title=f"Top 15 {x_col.replace('_', ' ').title()} (by Count)",
                           color_discrete_sequence=['#3498db'])
                fig.update_traces(marker_color='#3498db', marker_line_color='white', marker_line_width=0.5)
            else:
                # Default: first categorical or first column
                cat_cols = df.select_dtypes(include='object').columns
                target_col = cat_cols[0] if len(cat_cols) > 0 else df.columns[0]
                counts = df[target_col].value_counts().head(15).reset_index()
                counts.columns = [target_col, 'count']
                fig = px.bar(counts, x=target_col, y='count', 
                           title=f"Top 15 {target_col.replace('_', ' ').title()}",
                           color_discrete_sequence=['#3498db'])
                fig.update_traces(marker_color='#3498db', marker_line_color='white', marker_line_width=0.5)
                
        elif viz_type == 'line':
            if x_col and y_col:
                df_sorted = df_sample.sort_values(x_col)
                fig = px.line(df_sorted, x=x_col, y=y_col, 
                            title=f"{y_col.replace('_', ' ').title()} over {x_col.replace('_', ' ').title()}",
                            color_discrete_sequence=['#e74c3c'],  # Professional red
                            markers=True)
                fig.update_traces(line_color='#e74c3c', line_width=3, marker_color='#e74c3c', marker_size=6)
            else:
                num_cols = df.select_dtypes(include=[float, int]).columns
                if len(num_cols) > 0:
                    y_target = y_col if y_col else num_cols[0]
                    fig = px.line(df_sample, y=y_target, 
                                title=f"Trend of {y_target.replace('_', ' ').title()}",
                                color_discrete_sequence=['#e74c3c'],
                                markers=True)
                    fig.update_traces(line_color='#e74c3c', line_width=3, marker_color='#e74c3c', marker_size=6)
                else:
                    raise ValueError("No numeric columns for line plot")
                    
        elif viz_type == 'scatter':
            if x_col and y_col:
                fig = px.scatter(df_sample, x=x_col, y=y_col, 
                               title=f"Relationship: {x_col.replace('_', ' ').title()} vs {y_col.replace('_', ' ').title()}",
                               color_discrete_sequence=['#2ecc71'],  # Professional green
                               opacity=0.7)
                fig.update_traces(marker=dict(color='#2ecc71', size=8, opacity=0.7, line=dict(width=0.5, color='white')))
            else:
                num_cols = df.select_dtypes(include=[float, int]).columns
                if len(num_cols) >= 2:
                    x_target = x_col if x_col else num_cols[0]
                    y_target = y_col if y_col else num_cols[1]
                    fig = px.scatter(df_sample, x=x_target, y=y_target, 
                                   title=f"{x_target.replace('_', ' ').title()} vs {y_target.replace('_', ' ').title()}",
                                   color_discrete_sequence=['#2ecc71'],
                                   opacity=0.7)
                    fig.update_traces(marker=dict(color='#2ecc71', size=8, opacity=0.7, line=dict(width=0.5, color='white')))
                else:
                    raise ValueError("Need at least 2 numeric columns for scatter plot")
                    
        elif viz_type == 'histogram':
            if x_col:
                fig = px.histogram(df_sample, x=x_col, 
                                 title=f"Distribution of {x_col.replace('_', ' ').title()}",
                                 color_discrete_sequence=['#9b59b6'],  # Professional purple
                                 nbins=30)
                fig.update_traces(marker=dict(color='#9b59b6', line=dict(width=0.5, color='white')))
            else:
                num_cols = df.select_dtypes(include=[float, int]).columns
                target = num_cols[0] if len(num_cols) > 0 else df.columns[0]
                fig = px.histogram(df_sample, x=target, 
                                 title=f"Distribution of {target.replace('_', ' ').title()}",
                                 color_discrete_sequence=['#9b59b6'],
                                 nbins=30)
                fig.update_traces(marker=dict(color='#9b59b6', line=dict(width=0.5, color='white')))
                
        elif viz_type == 'box':
            if y_col:
                fig = px.box(df_sample, y=y_col, x=x_col if x_col else None, 
                            title=f"Box Plot of {y_col}" + (f" by {x_col}" if x_col else ""),
                            color_discrete_sequence=['#e67e22'])  # Professional orange
                fig.update_traces(marker_color='#e67e22', line_color='#d35400')
            else:
                num_cols = df.select_dtypes(include=[float, int]).columns
                if len(num_cols) > 0:
                    fig = px.box(df_sample, y=num_cols[0], 
                               title=f"Box Plot of {num_cols[0]}",
                               color_discrete_sequence=['#e67e22'])
                    fig.update_traces(marker_color='#e67e22', line_color='#d35400')
                else:
                    raise ValueError("Need numeric column for box plot")
                    
        elif viz_type == 'violin':
            if y_col:
                fig = px.violin(df_sample, y=y_col, x=x_col if x_col else None,
                               title=f"Violin Plot of {y_col}" + (f" by {x_col}" if x_col else ""),
                               color_discrete_sequence=['#1abc9c'])  # Professional teal
                fig.update_traces(marker_color='#1abc9c', line_color='#16a085')
            else:
                num_cols = df.select_dtypes(include=[float, int]).columns
                if len(num_cols) > 0:
                    fig = px.violin(df_sample, y=num_cols[0], 
                                  title=f"Violin Plot of {num_cols[0]}",
                                  color_discrete_sequence=['#1abc9c'])
                    fig.update_traces(marker_color='#1abc9c', line_color='#16a085')
                else:
                    raise ValueError("Need numeric column for violin plot")
                    
        elif viz_type == 'heatmap':
            # For heatmap, use correlation matrix of numeric columns
            num_cols = df.select_dtypes(include=[float, int]).columns
            if len(num_cols) >= 2:
                corr = df[num_cols].corr()
                fig = px.imshow(corr, text_auto=True, aspect="auto", 
                               title="Correlation Heatmap",
                               color_continuous_scale='RdBu_r')
            else:
                raise ValueError("Need at least 2 numeric columns for heatmap")
                
        elif viz_type == 'pie':
            if x_col:
                counts = df[x_col].value_counts().reset_index()
                counts.columns = [x_col, 'count']
                fig = px.pie(counts.head(10), values='count', names=x_col, 
                            title=f"Distribution of {x_col}")
            else:
                cat_cols = df.select_dtypes(include='object').columns
                target = cat_cols[0] if len(cat_cols) > 0 else df.columns[0]
                counts = df[target].value_counts().reset_index()
                counts.columns = [target, 'count']
                fig = px.pie(counts.head(10), values='count', names=target,
                            title=f"Distribution of {target}")
        else:
            # Default fallback
            fig = px.bar(df_sample, x=df.columns[0], title=f"Default Chart: {df.columns[0]}")

        # Apply clean, professional styling (minimize chartjunk, maximize data-ink ratio)
        fig.update_layout(
            template="plotly_white",  # Clean white background
            font=dict(family="Arial, sans-serif", size=13, color='#2c3e50'),
            title=dict(
                font=dict(size=20, family="Arial, sans-serif", color='#2c3e50', weight='bold'),
                x=0.5,  # Center title
                xanchor='center'
            ),
            showlegend=True if viz_type in ['scatter', 'line', 'bar'] else 'auto',
            legend=dict(
                font=dict(size=12),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#cccccc',
                borderwidth=1
            ),
            margin=dict(l=80, r=40, t=100, b=80),
            height=550,
            # Minimize grid lines (reduce chartjunk)
            xaxis=dict(
                showgrid=False,  # No vertical gridlines for cleaner look
                title_font=dict(size=14, color='#34495e'),
                tickfont=dict(size=12, color='#2c3e50'),
                tickangle=-45 if viz_type == 'bar' else 0,  # Rotate labels for bar charts
                showline=True,
                linewidth=1,
                linecolor='#cccccc'
            ),
            yaxis=dict(
                showgrid=True,   # Keep horizontal gridlines for readability
                gridcolor='#e8e8e8',
                gridwidth=0.5,
                title_font=dict(size=14, color='#34495e'),
                tickfont=dict(size=12, color='#2c3e50'),
                showline=True,
                linewidth=1,
                linecolor='#cccccc'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Use professional color schemes
        if viz_type in ['bar', 'scatter', 'line']:
            fig.update_traces(
                marker=dict(
                    line=dict(width=0.5, color='white')  # Add subtle borders
                ) if viz_type == 'bar' else {},
                line=dict(width=3) if viz_type == 'line' else {}
            )
        
        # Format hover data for better readability
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>%{y:,.2f}<extra></extra>' if viz_type != 'pie' else None
        )
        
        return fig
        
    except Exception as e:
        # Ultimate fallback
        fig = px.bar(x=['Error'], y=[1], title=f"Error: {str(e)}")
        return fig


def generate_visualization(df: pd.DataFrame, viz_type: str, x_col: Optional[str] = None, y_col: Optional[str] = None) -> plt.Figure:
    """
    Generate a matplotlib visualization (legacy function, kept for compatibility).

    Args:
        df (pd.DataFrame): Dataset.
        viz_type (str): Type of visualization (bar, line, scatter, histogram).
        x_col (str, optional): X-axis column.
        y_col (str, optional): Y-axis column.

    Returns:
        plt.Figure: Matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if viz_type == 'bar':
        if x_col and y_col:
            sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
        else:
            cat_col = df.select_dtypes(include='object').columns[0] if len(df.select_dtypes(include='object').columns) > 0 else df.columns[0]
            df[cat_col].value_counts().head(15).plot(kind='bar', ax=ax)
    elif viz_type == 'line':
        if x_col and y_col:
            sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
        else:
            num_col = df.select_dtypes(include=[float, int]).columns[0]
            df[num_col].plot(kind='line', ax=ax)
    elif viz_type == 'scatter':
        if x_col and y_col:
            sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
        else:
            num_cols = df.select_dtypes(include=[float, int]).columns
            if len(num_cols) >= 2:
                sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1], ax=ax)
    elif viz_type == 'histogram':
        if x_col:
            sns.histplot(data=df, x=x_col, ax=ax)
        else:
            num_col = df.select_dtypes(include=[float, int]).columns[0]
            sns.histplot(data=df, x=num_col, ax=ax)

    ax.set_title(f'{viz_type.capitalize()} Chart')
    plt.tight_layout()
    return fig
