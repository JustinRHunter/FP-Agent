#!/usr/bin/env python3
"""
SOA Financial Analysis Utilities

A comprehensive module for Australian financial advice calculations.
Includes investment product classes and utility functions for SOA analysis.

Author: AI Assistant
Date: 2025
Purpose: Support AI agents in creating compliant Australian SOA documents
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

# Australian Tax Constants (2024-25)
TAX_BRACKETS = [
    (18200, 0.0),
    (45000, 0.19),
    (120000, 0.325),
    (180000, 0.37),
    (float('inf'), 0.45)
]

MEDICARE_LEVY = 0.02
SUPER_GUARANTEE = 0.115  # 11.5% for 2024-25
CONCESSIONAL_CAP = 30000  # Annual concessional contribution cap
SUPER_TAX_RATE = 0.15
FRANKING_RATE = 0.30  # Company tax rate for franking credits

class AssetClass(Enum):
    """Investment asset classes"""
    CASH = "Cash"
    FIXED_INCOME = "Fixed Income"
    AUSTRALIAN_SHARES = "Australian Shares"
    INTERNATIONAL_SHARES = "International Shares"
    PROPERTY = "Property"
    ALTERNATIVES = "Alternatives"

class ProductType(Enum):
    """Investment product types"""
    MANAGED_FUND = "Managed Fund"
    ETF = "ETF"
    DIRECT_SHARES = "Direct Shares"
    TERM_DEPOSIT = "Term Deposit"
    CASH_ACCOUNT = "Cash Account"
    PLATFORM_INVESTMENT = "Platform Investment"

@dataclass
class InvestmentProduct:
    """Base class for investment products"""
    name: str
    product_type: ProductType
    asset_class: AssetClass
    management_fee: float  # Annual percentage (e.g., 0.0075 for 0.75%)
    expected_return: float  # Annual percentage before fees
    risk_level: str  # "Low", "Medium", "High"
    minimum_investment: float = 0
    franking_yield: float = 0  # For Australian shares
    liquidity_days: int = 1  # Days to access funds
    
    def annual_fee_dollars(self, investment_amount: float) -> float:
        """Calculate annual fee in dollars"""
        return investment_amount * self.management_fee
    
    def net_expected_return(self) -> float:
        """Expected return after management fees"""
        return self.expected_return - self.management_fee
    
    def after_tax_return(self, marginal_tax_rate: float) -> float:
        """Calculate after-tax return including franking credits"""
        gross_return = self.net_expected_return()
        
        if self.asset_class == AssetClass.AUSTRALIAN_SHARES and self.franking_yield > 0:
            # Include franking credit benefit
            franking_credit = self.franking_yield * (FRANKING_RATE / (1 - FRANKING_RATE))
            gross_income = self.franking_yield + franking_credit
            tax_on_income = gross_income * marginal_tax_rate
            net_franked_income = self.franking_yield + franking_credit - tax_on_income
            
            # Assume remaining return is capital growth (50% discount)
            capital_growth = gross_return - self.franking_yield
            tax_on_capital = capital_growth * marginal_tax_rate * 0.5  # CGT discount
            net_capital = capital_growth - tax_on_capital
            
            return net_franked_income + net_capital
        else:
            # Simple after-tax calculation
            return gross_return * (1 - marginal_tax_rate)

@dataclass
class Platform:
    """Investment platform with fee structure"""
    name: str
    admin_fee_percentage: float  # Annual admin fee as percentage
    admin_fee_fixed: float  # Fixed annual admin fee in dollars
    transaction_fee: float  # Per transaction fee
    min_balance: float = 0
    max_admin_fee: float = float('inf')  # Cap on percentage-based fees
    
    def annual_admin_fee(self, balance: float) -> float:
        """Calculate total annual admin fee"""
        percentage_fee = min(balance * self.admin_fee_percentage, self.max_admin_fee)
        return percentage_fee + self.admin_fee_fixed

# Pre-defined common investment products
COMMON_PRODUCTS = {
    'vanguard_balanced': InvestmentProduct(
        name="Vanguard Balanced Index Fund",
        product_type=ProductType.MANAGED_FUND,
        asset_class=AssetClass.AUSTRALIAN_SHARES,  # Mixed, but primarily
        management_fee=0.0029,  # 0.29%
        expected_return=0.07,  # 7% p.a.
        risk_level="Medium",
        minimum_investment=5000,
        franking_yield=0.035,  # 3.5% franked yield
        liquidity_days=3
    ),
    'vgs_international': InvestmentProduct(
        name="Vanguard International Shares ETF (VGS)",
        product_type=ProductType.ETF,
        asset_class=AssetClass.INTERNATIONAL_SHARES,
        management_fee=0.0018,  # 0.18%
        expected_return=0.08,  # 8% p.a.
        risk_level="High",
        minimum_investment=100,
        franking_yield=0,
        liquidity_days=3
    ),
    'cash_hisa': InvestmentProduct(
        name="High Interest Savings Account",
        product_type=ProductType.CASH_ACCOUNT,
        asset_class=AssetClass.CASH,
        management_fee=0,
        expected_return=0.045,  # 4.5% p.a.
        risk_level="Low",
        minimum_investment=0,
        franking_yield=0,
        liquidity_days=0
    )
}

# Common platforms
COMMON_PLATFORMS = {
    'netwealth': Platform(
        name="Netwealth",
        admin_fee_percentage=0.0055,  # 0.55%
        admin_fee_fixed=0,
        transaction_fee=9.50,
        min_balance=25000,
        max_admin_fee=2750
    ),
    'macquarie_wrap': Platform(
        name="Macquarie Wrap",
        admin_fee_percentage=0.0077,  # 0.77%
        admin_fee_fixed=0,
        transaction_fee=22,
        min_balance=25000,
        max_admin_fee=11000
    )
}

def calculate_marginal_tax_rate(annual_income: float, include_medicare: bool = True) -> float:
    """Calculate Australian marginal tax rate including Medicare levy"""
    for threshold, rate in TAX_BRACKETS:
        if annual_income <= threshold:
            marginal_rate = rate
            break
    
    if include_medicare:
        marginal_rate += MEDICARE_LEVY
    
    return marginal_rate

def future_value(present_value: float, annual_rate: float, years: float, 
                monthly_contribution: float = 0) -> float:
    """Calculate future value with optional regular contributions"""
    if annual_rate == 0:
        return present_value + (monthly_contribution * 12 * years)
    
    monthly_rate = annual_rate / 12
    months = years * 12
    
    # Future value of lump sum
    fv_lump = present_value * (1 + annual_rate) ** years
    
    # Future value of annuity (monthly contributions)
    if monthly_contribution > 0:
        fv_annuity = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    else:
        fv_annuity = 0
    
    return fv_lump + fv_annuity

def required_monthly_savings(target_amount: float, years: float, 
                           annual_return: float, current_savings: float = 0) -> float:
    """Calculate required monthly savings to reach a target"""
    if annual_return == 0:
        return (target_amount - current_savings) / (years * 12)
    
    monthly_rate = annual_return / 12
    months = years * 12
    
    # Future value of current savings
    fv_current = current_savings * (1 + annual_return) ** years
    
    # Amount still needed
    amount_needed = target_amount - fv_current
    
    if amount_needed <= 0:
        return 0
    
    # Required monthly payment
    return amount_needed / (((1 + monthly_rate) ** months - 1) / monthly_rate)

def super_contribution_benefit(contribution_amount: float, marginal_tax_rate: float) -> Dict[str, float]:
    """Calculate tax benefit of superannuation contributions"""
    # Ensure within contribution caps
    effective_contribution = min(contribution_amount, CONCESSIONAL_CAP)
    
    # Tax saved by contributing to super
    tax_saved = effective_contribution * (marginal_tax_rate - SUPER_TAX_RATE)
    
    # Net cost of contribution
    net_cost = effective_contribution - tax_saved
    
    return {
        'contribution_amount': effective_contribution,
        'tax_saved': tax_saved,
        'net_cost': net_cost,
        'tax_saving_rate': tax_saved / effective_contribution if effective_contribution > 0 else 0
    }

def break_even_analysis(switching_cost: float, annual_saving: float) -> Dict[str, float]:
    """Calculate break-even time for product switching"""
    if annual_saving <= 0:
        return {
            'break_even_years': float('inf'),
            'break_even_months': float('inf'),
            'worthwhile': False
        }
    
    break_even_years = switching_cost / annual_saving
    break_even_months = break_even_years * 12
    
    return {
        'break_even_years': break_even_years,
        'break_even_months': break_even_months,
        'worthwhile': break_even_years <= 3  # Arbitrary 3-year threshold
    }

def fee_impact_comparison(investment_amount: float, years: int, 
                         product1: InvestmentProduct, product2: InvestmentProduct) -> Dict[str, float]:
    """Compare long-term impact of fees between two products"""
    # Calculate final values
    final_value_1 = future_value(investment_amount, product1.net_expected_return(), years)
    final_value_2 = future_value(investment_amount, product2.net_expected_return(), years)
    
    # Approximate total fees paid over time
    avg_balance_1 = (investment_amount + final_value_1) / 2
    avg_balance_2 = (investment_amount + final_value_2) / 2
    total_fees_1 = avg_balance_1 * product1.management_fee * years
    total_fees_2 = avg_balance_2 * product2.management_fee * years
    
    return {
        'product1_final_value': final_value_1,
        'product2_final_value': final_value_2,
        'difference': final_value_2 - final_value_1,
        'product1_total_fees': total_fees_1,
        'product2_total_fees': total_fees_2,
        'fee_difference': total_fees_2 - total_fees_1
    }

def market_downturn_analysis(portfolio_value: float, downturn_percentage: float, 
                           recovery_years: int, annual_return: float) -> Dict[str, float]:
    """Analyze impact of market downturn and recovery time"""
    # Value after downturn
    value_after_downturn = portfolio_value * (1 - downturn_percentage)
    
    # Value after recovery period
    recovered_value = future_value(value_after_downturn, annual_return, recovery_years)
    
    # Time to break even (approximate)
    if annual_return > 0:
        break_even_years = math.log(portfolio_value / value_after_downturn) / math.log(1 + annual_return)
    else:
        break_even_years = float('inf')
    
    return {
        'original_value': portfolio_value,
        'value_after_downturn': value_after_downturn,
        'loss_amount': portfolio_value - value_after_downturn,
        'value_after_recovery': recovered_value,
        'break_even_years': break_even_years,
        'fully_recovered': recovered_value >= portfolio_value
    }

def asset_allocation_analysis(current_allocation: Dict[AssetClass, float], 
                            target_allocation: Dict[AssetClass, float],
                            total_portfolio_value: float) -> Dict[str, any]:
    """Analyze current vs target asset allocation"""
    rebalancing_required = {}
    total_rebalancing_amount = 0
    
    for asset_class in target_allocation:
        current_pct = current_allocation.get(asset_class, 0)
        target_pct = target_allocation[asset_class]
        difference_pct = target_pct - current_pct
        difference_dollars = difference_pct * total_portfolio_value
        
        rebalancing_required[asset_class] = {
            'current_percentage': current_pct,
            'target_percentage': target_pct,
            'difference_percentage': difference_pct,
            'difference_dollars': difference_dollars,
            'action': 'buy' if difference_dollars > 0 else 'sell' if difference_dollars < 0 else 'hold'
        }
        
        total_rebalancing_amount += abs(difference_dollars)
    
    return {
        'rebalancing_required': rebalancing_required,
        'total_rebalancing_amount': total_rebalancing_amount / 2,  # Divide by 2 as buys = sells
        'needs_rebalancing': total_rebalancing_amount > (total_portfolio_value * 0.05)  # 5% threshold
    }

def dollar_cost_averaging_vs_lump_sum(total_amount: float, years: float, 
                                    annual_return: float, volatility: float = 0.15) -> Dict[str, float]:
    """Compare dollar cost averaging vs lump sum investment"""
    # Lump sum investment
    lump_sum_final = future_value(total_amount, annual_return, years)
    
    # Dollar cost averaging (monthly)
    monthly_amount = total_amount / (years * 12)
    dca_final = future_value(0, annual_return, years, monthly_amount)
    
    # Simple volatility adjustment (rough approximation)
    volatility_benefit = total_amount * volatility * 0.5  # Rough estimate
    
    return {
        'lump_sum_final': lump_sum_final,
        'dca_final': dca_final,
        'difference': lump_sum_final - dca_final,
        'lump_sum_better': lump_sum_final > dca_final,
        'volatility_benefit_estimate': volatility_benefit
    }

def retirement_adequacy_analysis(current_age: int, retirement_age: int, 
                               current_super: float, annual_contribution: float,
                               annual_return: float, desired_retirement_income: float) -> Dict[str, float]:
    """Analyze retirement adequacy"""
    years_to_retirement = retirement_age - current_age
    
    # Project superannuation balance at retirement
    projected_super = future_value(current_super, annual_return, years_to_retirement, annual_contribution / 12)
    
    # Required balance for desired income (using 4% rule)
    required_balance = desired_retirement_income / 0.04
    
    # Shortfall or surplus
    shortfall = required_balance - projected_super
    
    # Additional monthly savings required
    if shortfall > 0:
        additional_monthly = required_monthly_savings(shortfall, years_to_retirement, annual_return)
    else:
        additional_monthly = 0
    
    return {
        'years_to_retirement': years_to_retirement,
        'projected_super_balance': projected_super,
        'required_balance': required_balance,
        'shortfall': max(0, shortfall),
        'surplus': max(0, -shortfall),
        'additional_monthly_required': additional_monthly,
        'on_track': shortfall <= 0
    }
