def generate_annaul_report_plot(self, year=None):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from collections import defaultdict
 
        classrooms = self.load_classroom_by_year(year) if year else self.load_classroom()
        if not classrooms:
            print("No classrooms found.")
            return
 
        all_students = [s for c in classrooms for s in c.students]
        if not all_students:
            print("No student found.")
            return
 
        active_classes = [c for c in classrooms if c.students]
 
        # Chart 1: best class per grade level (e.g. 7A, 8B, 9A...)
        classes_by_level = defaultdict(list)
        for c in active_classes:
            classes_by_level[c.class_level].append(c)
 
        level_labels   = []
        top_class_avgs = []
        top_class_ids  = []
        for level, classes in sorted(classes_by_level.items()):
            best = max(classes, key=lambda c: c.class_average())
            level_labels.append(level)
            top_class_avgs.append(best.class_average())
            top_class_ids.append(best.class_id)
 
        # Chart 2: top student per class (within the selected year)
        top_scores = []
        top_labels = []
        for c in sorted(active_classes, key=lambda c: c.class_level):
            top = max(c.students, key=lambda s: s.overall_average())
            top_scores.append(top.overall_average())
            top_labels.append(f"{c.class_id} {c.class_level} - {top.name}")
 
        # Chart 3: grade distribution school-wide
        grade_labels = ["A", "B", "C", "D", "E", "F"]
        grade_counts = {g: 0 for g in grade_labels}
        for s in all_students:
            grade_counts[s.grade_letter()] += 1
 
        title_label  = year if year else "All Years"
        chart2_height = max(6, len(active_classes) * 0.4)
 
        fig, axs = plt.subplots(3, 1, figsize=(12, 12 + chart2_height))
        fig.suptitle(f"Annual School Report — {title_label}", fontsize=15, fontweight="bold")
 
        # Chart 1: best class per grade level
        axs[0].bar(level_labels, top_class_avgs,
                   color=[self._score_color(v) for v in top_class_avgs])
        axs[0].set_ylim(min(top_class_avgs) - 10, 100)
        axs[0].set_title("Best Class per Grade Level")
        axs[0].set_ylabel("Average Score")
        axs[0].axhline(y=50, color="red", linestyle="--", label="Pass Mark")
        axs[0].legend()
        for i, (v, cid) in enumerate(zip(top_class_avgs, top_class_ids)):
            axs[0].text(i, v + 1, f"{v:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
            axs[0].text(i, v / 2, cid, ha="center", va="center", fontsize=8, fontweight="bold", color="white", rotation=90)
 
        # Chart 2: top student per class
        axs[1].barh(range(len(top_labels)), top_scores,
                    color=[self._score_color(v) for v in top_scores])
        axs[1].set_yticks(range(len(top_labels)))
        axs[1].set_yticklabels(top_labels, fontsize=9)
        axs[1].invert_yaxis()
        axs[1].axvline(x=50, color="red",   linestyle="--", label="Pass Mark")
        axs[1].axvline(x=70, color="green", linestyle=":",  label="Good (70)")
        axs[1].set_xlim(0, 100)
        axs[1].set_title("Top Student per Class")
        axs[1].set_xlabel("Overall Average Score")
        axs[1].legend()
        for i, v in enumerate(top_scores):
            axs[1].text(v + 1, i, f"{v:.1f}", va="center", fontsize=8, fontweight="bold")
 
        # Chart 3: grade distribution
        counts     = [grade_counts[g] for g in grade_labels]
        grd_colors = ["#2ecc71", "#27ae60", "#f1c40f", "#e67e22", "#e74c3c", "#c0392b"]
        axs[2].bar(grade_labels, counts, color=grd_colors)
        axs[2].set_title("School-wide Grade Distribution")
        axs[2].set_ylabel("Number of Students")
        for i, c in enumerate(counts):
            if c > 0:
                axs[2].text(i, c + 0.1, str(c), ha="center", fontsize=9, fontweight="bold")
 
        plt.tight_layout()
 
        filename = f"annual_report_{year.replace('-', '_')}.png" if year else "annual_report_all.png"
        return self._save_plot(plt, "annual", filename)
 
    def _score_color(self, value):
        if value >= 70:
            return "green"
        elif value >= 50:
            return "orange"
        return "red"
 
    def _save_plot(self, plt, folder, filename):
        save_dir = os.path.join("outputs", "graphs", folder)
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, filename)
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved to: {path}")
        return path