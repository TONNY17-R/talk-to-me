export const phq9Severity = (score) => {
  if (score <= 4) return { level: 'Minimal', color: '#10B981', interpretation: 'Minimal or no depression' };
  if (score <= 9) return { level: 'Mild', color: '#F59E0B', interpretation: 'Mild depression' };
  if (score <= 14) return { level: 'Moderate', color: '#F97316', interpretation: 'Moderate depression — consider counselling' };
  if (score <= 19) return { level: 'Moderately severe', color: '#DC2626', interpretation: 'Moderately severe depression — recommend professional help' };
  return { level: 'Severe', color: '#991B1B', interpretation: 'Severe depression — seek immediate professional support' };
};

export const gad7Severity = (score) => {
  if (score <= 4) return { level: 'Minimal', color: '#10B981', interpretation: 'Minimal or no anxiety' };
  if (score <= 9) return { level: 'Mild', color: '#F59E0B', interpretation: 'Mild anxiety' };
  if (score <= 14) return { level: 'Moderate', color: '#F97316', interpretation: 'Moderate anxiety — consider counselling' };
  return { level: 'Severe', color: '#DC2626', interpretation: 'Severe anxiety — seek professional support' };
};

export const saveAssessmentToLocal = (result) => {
  try {
    const existing = JSON.parse(localStorage.getItem('assessments') || '[]');
    existing.unshift({ ...result, savedAt: new Date().toISOString() });
    localStorage.setItem('assessments', JSON.stringify(existing.slice(0, 50)));
    return true;
  } catch (err) {
    console.error('saveAssessmentToLocal error', err);
    return false;
  }
};
