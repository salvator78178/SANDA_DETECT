# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'sanda_detect_2024_secret_key'

# Stockage des données en mémoire
declarations = []
modeles_ia = [
    {'id': 1, 'nom': 'RF_Classifier_v2.1', 'algorithme': 'Random Forest', 'performance': 94.2, 'statut': 'actif'},
    {'id': 2, 'nom': 'XGB_Fraud_v1.8', 'algorithme': 'XGBoost', 'performance': 89.7, 'statut': 'entrainement'},
    {'id': 3, 'nom': 'NN_DeepFraud_v3.0', 'algorithme': 'Réseau Neuronal', 'performance': 91.8, 'statut': 'archive'}
]

# Page d'accueil
@app.route('/')
@app.route('/home')
@app.route('/accueil')
def home():
    stats = {
        'total_declarations': len(declarations),
        'declarations_traitees': len([d for d in declarations if d.get('statut') == 'traite']),
        'alertes_fraude': len([d for d in declarations if d.get('statut') == 'alerte_fraude']),
        'declarations_actives': len([d for d in declarations if d.get('statut') in ['soumis', 'en_cours']])
    }
    return render_template('home.html', stats=stats)

# Administration
@app.route('/admin')
def admin():
    stats = {
        'total_declarations': len(declarations),
        'declarations_traitees': len([d for d in declarations if d.get('statut') == 'traite']),
        'alertes_fraude': len([d for d in declarations if d.get('statut') == 'alerte_fraude'])
    }
    return render_template('admin.html', stats=stats)

# Analyste IA
@app.route('/analyste')
def analyste():
    stats_entrainement = {
        'total': len(declarations),
        'fraudes': len([d for d in declarations if d.get('statut') == 'alerte_fraude'])
    }
    return render_template('analyst.html', modeles=modeles_ia, donnees_entrainement=stats_entrainement)

# Agent Assurance
@app.route('/agent')
def agent():
    dossiers_attente = [d for d in declarations if d.get('statut') in ['soumis', 'en_cours']]
    alertes_fraude = [d for d in declarations if d.get('statut') == 'alerte_fraude']
    return render_template('agent.html',
                           dossiers_attente=dossiers_attente,
                           alertes_fraude=alertes_fraude)

# Espace Client
@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        try:
            # Récupération des données du formulaire
            nom = request.form.get('nom', '').strip()
            police = request.form.get('police', '').strip()
            email = request.form.get('email', '').strip()
            telephone = request.form.get('telephone', '').strip()
            date_sinistre = request.form.get('date_sinistre', '').strip()
            type_sinistre = request.form.get('type_sinistre', '').strip()
            description = request.form.get('description', '').strip()

            # Validation
            if not nom or not police or not description:
                flash('Veuillez remplir tous les champs obligatoires (Nom, Police, Description).', 'error')
                return render_template('client.html')

            # Création de la déclaration
            nouvelle_declaration = {
                'id': len(declarations) + 1,
                'nom_complet': nom,
                'numero_police': police,
                'email': email,
                'telephone': telephone,
                'date_sinistre': date_sinistre,
                'type_sinistre': type_sinistre,
                'description': description,
                'statut': 'soumis',
                'date_creation': datetime.now().strftime('%d/%m/%Y %H:%M')
            }

            # Analyse simple de fraude
            if analyser_risque_fraude(description):
                nouvelle_declaration['statut'] = 'alerte_fraude'
                flash('⚠️ Votre déclaration a été reçue et est en analyse approfondie.', 'warning')
            else:
                flash('✅ Votre déclaration de sinistre a été envoyée avec succès!', 'success')

            declarations.append(nouvelle_declaration)
            return redirect(url_for('client'))

        except Exception as e:
            flash('Une erreur est survenue lors de l\'envoi de la déclaration.', 'error')

    # Filtrer les déclarations de l'utilisateur actuel (simulation)
    declarations_utilisateur = [d for d in declarations if d.get('nom_complet')]
    return render_template('client.html', declarations=declarations_utilisateur[-10:])

def analyser_risque_fraude(description):
    """Simulation d'analyse de fraude"""
    mots_suspects = ['accident', 'vol', 'cambriolage', 'incendie', 'témoin', 'blessé']
    description_lower = description.lower()
    
    score = sum(1 for mot in mots_suspects if mot in description_lower)
    return score >= 2

# API pour les statistiques
@app.route('/api/stats')
def get_stats():
    total = len(declarations)
    fraudes = len([d for d in declarations if d.get('statut') == 'alerte_fraude'])
    taux_fraude = (fraudes / total * 100) if total > 0 else 0
    
    return jsonify({
        'total_declarations': total,
        'declarations_actives': len([d for d in declarations if d.get('statut') in ['soumis', 'en_cours']]),
        'taux_fraude': f"{taux_fraude:.1f}%"
    })

# Gestion des erreurs
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SANDA_DETECT - Système de Détection de Fraude")
    print("📧 Développé pour le mémoire de fin d'études")
    print("🌐 Application démarrée sur: http://localhost:5000")
    print("💾 Mode: Mémoire (pas de base de données)")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)