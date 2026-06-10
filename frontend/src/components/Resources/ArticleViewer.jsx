import React from 'react';

export const ArticleViewer = ({ article }) => {
  return (
    <div className="article-viewer">
      <h2>{article.title}</h2>
      <p className="article-meta">By {article.author} | {article.date}</p>
      <div className="article-content" dangerouslySetInnerHTML={{ __html: article.content }} />
    </div>
  );
};
