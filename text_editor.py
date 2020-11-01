# Η εφαρμογή MyEdit

import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
#import os


class MyEdit():
    ''' Η κλάση που σχεδιάζει τα γραφικά - περιλαμβάνει μεθόδους για βασικές επιλογές'''

    def __init__(self, root):
        self.root = root
        self.filename = None
        self.root.geometry('800x600')
        # self.root.resizable(False, False)
        self.fnt = 'Arial '
        self.fnt_size = 20
        self.f0 = tk.Frame(self.root, relief='raised', padx=2, pady=2, width=800, height=20)
        self.f0.pack(side='top', fill='x')
        self.f1 = tk.Frame(self.root, padx=2, pady=2, width=800)
        self.f1.pack(side='top', expand=True, fill='both')
        self.makewidgets()
        self.fname = None

    def makewidgets(self):
        tk.Button(self.f0, font=self.fnt, text='Νέο ..', command=self.new).pack(side='left',
                                                                                expand=1, fill='both')
        tk.Button(self.f0, font=self.fnt, text='Άνοιγμα ..', command=self.file).pack(side='left',
                                                                                     expand=1, fill='both')
        tk.Button(self.f0, font=self.fnt, text='Αποθήκευση ..', command=self.save).pack(side='left',
                                                                                        expand=1, fill='both')
        tk.Button(self.f0, font=self.fnt, text='Χρώμα ..', command=self.color).pack(side='left',
                                                                                    expand=1, fill='both')
        tk.Button(self.f0, font=self.fnt, text=' + ', command=self.bigger).pack(side='left',
                                                                                expand=1, fill='both')
        tk.Button(self.f0, font=self.fnt, text=' - ', command=self.smaller).pack(side='left',
                                                                                 expand=1, fill='both')
        self.term = tk.Entry(self.f0, bg='lightblue', width=30, font=self.fnt)
        self.term.insert(0, '⌕')
        self.term.pack(expand=1, fill='x')
        # δημιουργία μπάρας κύλισης
        self.sbar = tk.Scrollbar(self.f1)
        self.text = tk.Text(self.f1, relief='sunken')
        self.sbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.sbar.set)
        self.sbar.pack(side='right', fill='y')
        self.text.pack(side='left', expand=1, fill='both')

        # διαχείριση του πλαισίου term
        self.term.bind('<FocusIn>', lambda e: self.term.delete(0.30))
        self.term.bind('<Return>', self.search)
        self.text.tag_config('found', background='yellow')


    def search(self, event):
        indx = '1.0'
        term = self.term.get()
        self.text.tag_remove('found', '1.0', 'end')
        while True:
            indx = self.text.search(term, indx, nocase=True, stopindex='end')
            if not indx:
                break
            endindx = '{}+{}c'.format(indx, len(term))
            self.text.tag_add('found', indx, endindx)
            indx = endindx
        print(self.text.tag_ranges('found'))

    def new(self):
        self.text.delete('1.0', 'end')
        self.root.title('MyEdit v 0.1')
        self.text.config(bg='white')
        self.fnt_size = 20


    def file_open(self):
        self.filename = filedialog.askopenfilename()
        self.set_text()

    def file(self):
        self.fname = filedialog.askopenfilename()
        self.set_text()

    def save(self):  # 2. save
        try:
            f = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
            if f is None_:  # η περίπτωση που άλλαξε γνώμη και δεν αποθήκευσε το αρχείο
                return
            f.write(self.gettext())
            f.close()
            self.text.delete('1.0', 'end')
            messagebox.showinfo('Info', 'Το αρχείο αποθηκεύτηκε επιτυχώς')
        except:
            messagebox.showinfo('Info', 'Σφάλμα κατά την αποθήκευση του αρχείου!')


    def gettext(self):  # επιστρέφει το αρχείο που υπάρχει στο text
        return self.text.get('1.0', 'end' + '-1c')  #


    def color(self):
        self.color = colorchooser.askcolor(title='Επιλογή χρώματος')
        print(self.color)
        self.text.config(bg=self.color[-1])


    def bigger(self):
        self.fnt_size += 2
        self.set_font()


    def smaller(self):
        self.fnt_size -= 2
        self.set_font()


    def set_font(self):
        if self.fnt_size < 10: self.fnt_size = 10
        if self.fnt_size > 40: self.fnt_size = 40
        font = self.fnt + str(self.fnt_size)
        self.text.config(font=font)


    def set_text(self):
        if self.filename:  # Αν ο χρήστης δε βάλει αρχείο txt.
            try:
                text = open(self.filename, 'r').read()
            except:
                messagebox.showinfo('Προσοχή!', 'Το MyEdit ανοίγει μόνο αρχεία κειμένου')
            else:
                self.text.delete('1.0', 'end')  # διαγραφή περιεχομένου
                self.text.insert('1.0', text)  # εισαγωγή νέου κειμένου
                self.set_font()
                self.text.nark_set('insert', '1.0')  # θέσε δρομέα στην αρχική θέση
                self.text.focus()  # εστίαση στο κείμενο
                self.root.title('MyEdit: ' + self.filename)


if __name__ == '__main__':
    root = tk.Tk()
    MyEdit(root)
    root.mainloop()
