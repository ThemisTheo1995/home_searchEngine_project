function showNotes(pk) {
    const notesSection = document.getElementById('notesSection'+pk);
    if (notesSection.classList.contains('hidden')) {
        notesSection.classList.remove('hidden');
    } else {
        notesSection.classList.add('hidden');
    }
}
