#!/usr/bin/env python3
"""
Command Line Interface for the Financial Figures Agent
Provides interactive access to figure information and analysis
"""
import argparse
import sys
from demo import FinancialFiguresAgentDemo
from main import FinancialFiguresAgent

def main():
    parser = argparse.ArgumentParser(description='Financial Markets Key Figures Intelligence Agent')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (no API key required)')
    parser.add_argument('--list-categories', action='store_true', help='List all available categories')
    parser.add_argument('--list-figures', metavar='CATEGORY', help='List figures in a specific category')
    parser.add_argument('--analyze', metavar='FIGURE_NAME', help='Analyze market influence of a specific figure')
    parser.add_argument('--report', metavar='CATEGORY', nargs='?', const='all', help='Generate market report for category (or all)')
    parser.add_argument('--info', metavar='FIGURE_NAME', help='Get detailed information about a figure')
    
    args = parser.parse_args()
    
    # Initialize agent
    if args.demo:
        agent = FinancialFiguresAgentDemo()
        print("🔧 Running in DEMO mode (no API key required)")
    else:
        try:
            agent = FinancialFiguresAgent()
            print("🔑 Running with OpenAI API integration")
        except Exception as e:
            print(f"❌ Error initializing OpenAI agent: {e}")
            print("💡 Use --demo flag to run without API key")
            sys.exit(1)
    
    print("🏦 Financial Markets Key Figures Intelligence Agent")
    print("=" * 55)
    
    # Handle commands
    if args.list_categories:
        print("\n📋 Available Categories:")
        for i, category in enumerate(agent.get_all_categories(), 1):
            figures_count = len(agent.list_figures_by_category(category))
            print(f"{i:2d}. {category.replace('_', ' ').title()} ({figures_count} figures)")
    
    elif args.list_figures:
        category = args.list_figures
        figures = agent.list_figures_by_category(category)
        if figures:
            print(f"\n👥 {category.replace('_', ' ').title()} ({len(figures)} figures):")
            for i, figure in enumerate(figures, 1):
                info = agent.get_figure_info(figure, category)
                print(f"{i:2d}. {figure} - {info['institution']}")
        else:
            print(f"❌ Category '{category}' not found")
            print("💡 Use --list-categories to see available categories")
    
    elif args.info:
        figure_name = args.info
        info = agent.get_figure_info(figure_name)
        if info:
            print(f"\n👤 {figure_name}")
            print(f"Position: {info['position']}")
            print(f"Institution: {info['institution']}")
            print(f"Country: {info['country']}")
            print(f"Influence Areas: {', '.join(info['influence_areas'])}")
        else:
            print(f"❌ Figure '{figure_name}' not found")
    
    elif args.analyze:
        figure_name = args.analyze
        print(f"\n🔍 Analyzing market influence: {figure_name}")
        print("-" * 50)
        analysis = agent.analyze_market_influence(figure_name)
        print(analysis)
    
    elif args.report:
        category = args.report if args.report != 'all' else None
        print(f"\n📊 Generating market report{'for ' + category if category else ''}...")
        print("-" * 50)
        report = agent.generate_market_update_report(category)
        print(report)
    
    else:
        # Default interactive mode
        print(f"\n📊 Monitoring {sum(len(cat) for cat in agent.key_figures.values())} key figures")
        print(f"📋 Categories: {len(agent.get_all_categories())} sectors")
        print("\n💡 Use --help for command options or run interactively:")
        
        while True:
            try:
                print("\n" + "="*40)
                print("Options:")
                print("1. List categories")
                print("2. List figures in category")
                print("3. Get figure information")
                print("4. Analyze market influence")
                print("5. Generate market report")
                print("6. Exit")
                
                choice = input("\nSelect option (1-6): ").strip()
                
                if choice == '1':
                    print("\n📋 Categories:")
                    for i, cat in enumerate(agent.get_all_categories(), 1):
                        count = len(agent.list_figures_by_category(cat))
                        print(f"{i}. {cat.replace('_', ' ').title()} ({count} figures)")
                
                elif choice == '2':
                    category = input("Enter category name: ").strip()
                    figures = agent.list_figures_by_category(category)
                    if figures:
                        print(f"\n👥 {category.replace('_', ' ').title()}:")
                        for i, fig in enumerate(figures, 1):
                            info = agent.get_figure_info(fig, category)
                            print(f"{i}. {fig} - {info['institution']}")
                    else:
                        print("❌ Category not found")
                
                elif choice == '3':
                    name = input("Enter figure name: ").strip()
                    info = agent.get_figure_info(name)
                    if info:
                        print(f"\n👤 {name}")
                        print(f"Position: {info['position']}")
                        print(f"Institution: {info['institution']}")
                        print(f"Influence: {', '.join(info['influence_areas'])}")
                    else:
                        print("❌ Figure not found")
                
                elif choice == '4':
                    name = input("Enter figure name for analysis: ").strip()
                    print(f"\n🔍 Analyzing {name}...")
                    print(agent.analyze_market_influence(name))
                
                elif choice == '5':
                    category = input("Enter category (or press Enter for all): ").strip()
                    category = category if category else None
                    print("\n📊 Generating report...")
                    print(agent.generate_market_update_report(category))
                
                elif choice == '6':
                    print("👋 Goodbye!")
                    break
                
                else:
                    print("❌ Invalid option")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()