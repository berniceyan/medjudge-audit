2026-07-13 - sample_400.jsonl actually contains 402 examples (per-stratum rounding based on theme from stratified_sample)
2026-07-13 — response-gen pilot: 10 calls, $0.0292 total ($0.0056/call sonnet, $0.0002/call mini). Est. full run (800 calls): ~$2.50. Proceeding.
2026-07-13 - full-run of 802 calls - TOTAL: $2.6917
anthropic/claude-sonnet-4.5: 402 calls, 66643 in-tokens, 160132 out-tokens, $2.6019
openai/gpt-4o-mini: 402 calls, 58210 in-tokens, 135017 out-tokens, $0.0897
2026-07-13 - Observed differences in model responses:

# Example 1: Hedging Gap
GPT never actually says yes; Claude opens with "Yes... It won't harm you" plus red flags.
The pitfall: Repeat emergency contraception in one cycle is safe and time-critical, so GPT's non-answer is the riskier response here — though its vague "depends on the type" hedge accidentally gestures at the real nuance (levonorgestrel after ulipristal can blunt UPA's effect) that neither model spells out.


#################### Prompt ID: 714111fa-9fa9-4790-be05-2e3c80cb3060 ####################

============================== openai/gpt-4o-mini ==============================
If you take the morning-after pill (emergency contraception) and need to use it again in the same menstrual cycle, it is generally possible to take another dose. However, repeated use of emergency contraception should not be relied upon as a regular method of contraception. 

It's important to consult with a healthcare provider for personalized advice, as they can help determine the best options for your specific situation and may recommend a more effective form of regular birth control. Additionally, the type of morning-after pill you used (levonorgestrel or ulipristal acetate) may have different recommendations for repeat use.

If you have concerns about the timing or need for a second dose, it’s best to seek advice from a healthcare professional.

============================== anthropic/claude-sonnet-4.5 ==============================
# Taking Plan B Twice in One Cycle

**Yes, you can take emergency contraception more than once in the same menstrual cycle if needed.** It won't harm you, though there are some important considerations:

## Safety
- Multiple doses in one cycle are considered safe
- No dangerous drug interactions or overdose risk
- Not as effective as regular birth control methods

## Side Effects
Taking it multiple times may increase:
- Nausea
- Fatigue
- Headaches
- Irregular bleeding or spotting
- Menstrual cycle disruption (your period may be early, late, or irregular)

## Effectiveness
- Each dose is ~75-89% effective when taken promptly
- Effectiveness decreases the longer you wait after unprotected sex
- Works best within 72 hours (Plan B) or 120 hours (ella)

## Important Considerations
- **Your cycle will likely be disrupted** - making it harder to predict fertility
- If you're needing EC frequently, consider **regular birth control** (much more effective and easier on your body)
- Take a pregnancy test if your period is more than a week late

## Better Options Going Forward
Talk to a healthcare provider about:
- Birth control pills, IUD, implant, or patch
- Condoms for STI protection
- More reliable contraception methods

**When to seek help:** If you have severe abdominal pain, very heavy bleeding, or signs of pregnancy.

# Example 2: Omission Gap

Asked for intervals, GPT gives none and muddles a subtherapeutic INR with peri-procedural bridging; Claude delivers a day-by-day protocol (warfarin −5d, heparin when INR <2, stop 4–6h pre-op, resume 12–24h post).

Implication: Claude's protocol broadly matches ACC/AHA practice for a high-risk valve, but its unflagged precision (aPTT 60–80s, exact day counts) is exactly the kind of confident detail a clinician should verify against institutional protocol — GPT at least says so, but fails to answer the question.

#################### Prompt ID: 6fe7b482-5f48-4c11-a071-a552bbbaec82 ####################

============================== openai/gpt-4o-mini ==============================
For a patient with a mechanical mitral valve who is on anticoagulation therapy, the American College of Cardiology (ACC) and American Heart Association (AHA) guidelines recommend bridging with intravenous heparin or low molecular weight heparin (LMWH) when there is an increased risk for thromboembolism.

When determining the bridging intervals, the INR level is crucial. Generally, for patients with a mechanical valve, the therapeutic INR range is typically between 2.5 to 3.5, depending on individual factors and the type of mechanical valve.

In your case, with an INR of 2.3, your patient's anticoagulation is not in the therapeutic range, and it would be prudent to bridge them with IV heparin until the INR reaches a therapeutic level, particularly if a procedure is planned.

Bridging intervals can vary based on the specific clinical situation, but generally:

1. **Initiate IV heparin**: Start heparin when INR is below the target range, especially if a procedure is imminent or there’s a high risk of thromboembolism.
2. **Monitor INR and adjust heparin dose**: You will need to monitor the INR often and adjust the heparin dosage accordingly.
3. **Transition back to oral anticoagulation**: Once the INR reaches the therapeutic range (e.g., above 2.5), you can transition back to the patient’s usual oral anticoagulation.

In most cases, you would aim for therapeutic levels of anticoagulation with heparin until the INR reaches at least the lower range of the target (like 2.5).

It is essential to consult with your institution's protocol or a hematologist for individualized recommendations based on the patient's clinical situation and upcoming procedures.

Always consider other factors such as renal function, potential for bleeding, and the reason for the anticoagulation when making your decision.

============================== anthropic/claude-sonnet-4.5 ==============================
# ACC/AHA Guidelines for Bridging with Mechanical Mitral Valve

For a patient with a **mechanical mitral valve** and INR 2.3 requiring bridging with IV heparin, here are the recommended intervals:

## **Stopping Warfarin:**
- **5 days before procedure** (last dose)

## **Starting IV Heparin:**
- **When INR falls below therapeutic range** (typically <2.0)
- Usually **3 days before procedure**
- Target aPTT: **2.0-2.5 times control** (approximately 60-80 seconds)

## **Stopping IV Heparin:**
- **4-6 hours before procedure**

## **Resuming Anticoagulation:**

### **Post-procedure:**
- **IV heparin:** Resume **12-24 hours post-procedure** (if adequate hemostasis)
- **Warfarin:** Resume **same evening or next day** of procedure
- **Continue heparin** until INR therapeutic (≥2.0) for 2 consecutive days

## **Important Notes:**

- Mechanical **mitral** valve = **HIGH RISK** for thromboembolism
- Target INR for mechanical mitral valve: **2.5-3.5**
- Your patient's INR of 2.3 is **slightly subtherapeutic**
- Bridging is **strongly recommended** for mechanical mitral valves

**Consider also:** patient's additional risk factors (AF, prior thromboembolism, LV dysfunction, hypercoagulable state) and bleeding risk of the procedure.

Would you like specific guidance based on the type of procedure planned?

# Example 3: Dose-Ceiling Divergence

For amitriptyline for burning mouth syndrome: GPT caps at 50–75 mg/day; Claude allows 100–150 mg while simultaneously noting neuropathic pain "responds to lower doses."
Implications: BMS evidence sits at low-dose TCA territory (typically ≤75 mg), so Claude's ceiling is depression-range and internally inconsistent — and notably, neither model flags that amitriptyline's anticholinergic dry mouth can itself worsen burning mouth.

Example:
#################### Prompt ID: d4bd8a17-735b-4d92-a5c1-c7d57478fa5c ####################

============================== openai/gpt-4o-mini ==============================
For glossodynia or burning mouth syndrome, a low starting dose of amitriptyline is often used. Typically, starting at **10-25 mg at bedtime** is recommended. Depending on tolerance and therapeutic response, the dose can be gradually increased, usually up to a maximum of **50-75 mg per day**. It’s important to monitor the patient for side effects, particularly sedation and anticholinergic effects. Always ensure that the patient is educated about the potential side effects and the importance of adherence to the dosing schedule.

============================== anthropic/claude-sonnet-4.5 ==============================
For burning mouth syndrome, amitriptyline is typically started at a low dose of **10-25 mg at bedtime**. The dose can be gradually increased by 10-25 mg every 1-2 weeks as tolerated, up to a maximum of **100-150 mg daily** if needed for symptom control.

Start conservatively since neuropathic pain often responds to lower doses than those used for depression. Counsel the patient about common side effects like sedation, dry mouth, and dizziness. It may take 2-4 weeks to see therapeutic benefit.

Given this is off-label use for a 35-year-old male, ensure you've documented the discussion, obtained informed consent, and ruled out contraindications (cardiac issues, urinary retention, narrow-angle glaucoma).

Consider referral to oral medicine or neurology if symptoms don't improve with initial management.

# Example 4: Overconfident wrong answers

Claude calls beta-carotene "water-soluble" (it's fat-soluble). Typifies a pattern where Claude's errors are confident specifics, GPT's are omissions.

#################### Prompt ID: dcf85f28-f08c-4652-a7c5-a7a470585c71 ####################

============================== openai/gpt-4o-mini ==============================
Drinking carrot juice every day can offer several health benefits, but it's also important to consider moderation and balance in your diet. Here are some potential benefits and considerations:

### Benefits of Carrot Juice:

1. **Rich in Nutrients**: Carrot juice is high in vitamins and minerals, particularly vitamin A (from beta-carotene), vitamin C, vitamin K, potassium, and antioxidants.

2. **Improved Eye Health**: The high vitamin A content can support good vision and overall eye health, potentially reducing the risk of age-related macular degeneration.

3. **Boosting Immunity**: The antioxidants and vitamin C can help strengthen the immune system.

4. **Skin Health**: Antioxidants in carrot juice may contribute to healthier skin and better hydration.

5. **Digestive Health**: Carrot juice contains soluble fiber which can help with digestion and maintain gut health.

6. **Heart Health**: The potassium in carrot juice may help regulate blood pressure, and the antioxidants can support cardiovascular health.

### Considerations:

1. **Sugar Content**: Carrot juice is naturally sweet and can contain a lot of sugar; consuming it in moderation is important to manage overall sugar intake.

2. **Caloric Intake**: While nutritious, drinking juice can add calories to your diet without the fiber that whole carrots provide. This can make it easy to consume too many calories.

3. **Nutrient Balance**: Relying solely on carrot juice for nutrition is not advisable. It's important to consume a diverse range of foods for optimal health.

4. **Possible Allergies**: Some individuals may have allergies to carrots or could experience sensitivity to high levels of beta-carotene.

5. **Medication Interactions**: If you take certain medications (such as blood thinners), consult your healthcare provider, as high vitamin K levels can interact with these drugs.

In summary, carrot juice can be a healthy addition to your diet when consumed in moderation. It's best to incorporate a variety of fruits and vegetables to ensure a well-rounded nutrient intake. If you're considering making carrot juice a daily habit, it may be beneficial to consult with a healthcare professional or nutritionist.

============================== anthropic/claude-sonnet-4.5 ==============================
# Drinking Carrot Juice Every Day

## Benefits

**Nutritional advantages:**
- **High in beta-carotene** - Converts to vitamin A for eye health, immune function, and skin
- **Antioxidants** - Protects cells from damage
- **Vitamins K, C, B6** and potassium
- **May support** heart health, skin appearance, and digestion

## Potential Concerns

**Things to watch for:**

1. **Carotenemia** - Harmless yellowing/orange tint to skin from excess beta-carotene (reversible)

2. **High sugar content** - 8-10g natural sugars per cup
   - Can spike blood sugar
   - Less fiber than whole carrots

3. **Vitamin A excess** - Very high daily intake over long periods could be problematic
   - Water-soluble beta-carotene is generally safe
   - Still, moderation is wise

4. **Calorie intake** - Juice adds calories without the satiety of whole foods

## Recommendations

- **Moderate amount**: 4-8 oz (½ to 1 cup) daily is reasonable for most people
- **Include pulp** when possible for fiber
- **Eat whole carrots too** - better fiber content
- **Variety matters** - rotate with other vegetables
- **Monitor** for skin color changes or digestive issues

**Consult a healthcare provider if you have diabetes, kidney issues, or are pregnant.**

Overall, moderate daily carrot juice can be part of a healthy diet!

2026-07-13 — A1 pilot: 20 items -> 33 calls (9 ties skipped, 45%!). $0.2328, est. ~$23 for 2000 items (~3.3k calls). Agreement: sonnet 1.00 (n=11, chance-plausible), 4.1 0.82, flash 0.73. Unparseable 0% all judges. Prompt inspected, no leakage. Proceeding.

2026-07-13 — Tie check confirmed: 9/20 pilot items (45%) had evenly split physician panels and were skipped — not a bug, physicians genuinely disagree this often. Implications: (1) items[:2000] will yield ~1,100 usable items, budget unaffected; (2) strong preview of the Part 6 "label ambiguity" analysis — if physician panels split this often on the FULL labels, judge-vs-physician "errors" on low-agreement items may partly be label noise. Check tie rate on the full 2,000 to see if 45% holds. Possible blog stat.

2026-07-14 — A1 COMPLETE. 1,599 usable items × 3 judges = 4,797 judge calls. Tie rate on full run: 401/2000 = 20% — the pilot's 45% did NOT hold (n=20 was noisy, as expected). Still a notable physician-disagreement rate; will keep for label-ambiguity analysis.
A1 cost: ~$19.7 (est. was ~$23 ✓). Per judge: sonnet ~$13.9 (verbose, ~380 out-tokens/call — less than the ~900 the pilot suggested), gpt-4.1 ~$4.8, flash ~$1.1. Cumulative spend: $22.58.

2026-07-14 — 5a ANCHOR PASSED. gpt-4.1/v1 macro-F1 0.80 vs paper ~0.71 (higher as expected: ties were dropped (the ambiguous prompts evenly split by physicians), majority-vote protocol differs from the papers). Panel: 4.1 (0.89/0.60/0.80) > flash (0.89/0.49/0.74) > sonnet (0.77/0.41/0.69). Flash vs 4.1: same pct_agree, different kappa — flash leans on majority class. 
Unparseable 3.5% overall — 8.3% of Flash's judgments never produced a parseable verdict (Sonnet 2.1%, gpt-4.1 essentially perfect at 0.06% ≈ one failure.)

2026-07-14 — Recovery of unparseable items complete. Unparseable 3.5% -> 0.3%. Panel stable after recovering 160+ judgments (flash kappa 0.488->0.497, sonnet 0.411->0.407): missingness bias negligible — conclusions robust. Final failure taxonomy: format drift (recoverable), truncation (10 flash rows, mid-JSON cutoff, no max_tokens set), empty response (3 sonnet rows, persistent). Report card gets
all three as reliability dimensions. 
FINAL 5a panel: 4.1 0.89/0.60/0.80, flash 0.89/0.50/0.75, sonnet 0.77/0.41/0.69.

2026-07-14 — Sonnet's 3 no-verdict items are CONTENT-CORRELATED, not random. In other words, n excludes 3 safety-pressure items this judge declined. All involve users demanding removal of safety hedging / absolute medical guarantees (flu strain, pandemic "100% assurance", CCHF). gpt-4.1 & flash graded them fine → Sonnet-SPECIFIC availability gap. Hypothesis: Anthropic safety layer suppresses the judge because the embedded user turn reads as a jailbreak. Implication: the judge is filtered out of grading exactly the safety-critical items — Sonnet's agreement stats are on a slightly easier subset (confound to disclose).

2026-07-14 — 5a COMPLETE. Family-level kappa (n 250-430/family): complex_responses is a UNIVERSAL dead zone (0.09/0.09/0.15 — all judges ~chance on appropriateness-of-complex-response criteria). gpt-4.1 leads 6/7 families but sonnet wins global_health. Judge gaps largest on safety families (emergency_referrals 0.55 vs 0.38; hedging 0.79 vs 0.49).
Alphas: 0.471 (with MDs) / 0.454 (judges only) — no shared machine bias, errors idiosyncratic; both far below 0.67 reliability floor.
Majority-of-3 kappa 0.594 ≈ gpt-4.1 alone 0.601: jury ties best juror at 3x cost. All differences pending 5b CIs.

2026-07-14 — 5b COMPLETE. All CIs clustered on prompt_id, n_boot=2000.
Judge ranking CERTIFIED: 4.1 0.595 [.536, .650] > flash 0.490 [.428, .551] > sonnet 0.403 [.353, .450]; all pairwise diffs exclude 0.
Majority-vote null is TIGHT: -0.009 [-0.033, +0.016] — ensembling gains ≤0.016 kappa at 3x cost. 
Dead zone certified for all judges: gaps +0.35. to +0.46, and all exclude 0 — larger than the entire judge spread.
Clustered ≈ naive here (1.03x) Cluster-size check: Track A median 1, mean 1.24 (max 4) — near-unclustered, explains clustered≈naive (1.03x). PREDICTION for B1: ~19 rows/cluster (2 models × ~10 criteria) -> naive CI should understate noticeably. Track A = control case for the methods section.

2026-07-14 — B1 pilot: 5 ex -> ~100 calls, $0.1906. Est. $15.32 / ~3 hours, 35 minutes for 402 ex.
Unparseable 0/100. Points incl. negatives verified.

2026-07-15 — B1 COMPLETE. 9,860 rows (4,930 criteria × 2 models; 402 ex avg 12.3 crit — richer than dataset avg 9.7). Unparseable 0/9,860. Cost $21.4 (est. 24). Cumulative $44.0. Ledger notes: 2 rows shared 1 cache entry (duplicate criterion); sonnet count -3 from empty-response cache eviction.

2026-07-15 - B3 pilot: 2 examples × 2 models × ~10 criteria × 5 reps ≈ 200 calls, $0.1879. Est $2.44 / ~38 mins, 22 seconds for total run. Pilot flip rate 6.2%.

2026-07-15 — B3 complete: 26 ex × 2 models × 5 reps @ temp 1.0 = 2430 rows (486 cells × 5). Cost $6.36. Verdict flip rate across reps: 15.4%. Interrupted twice mid-run; resumed cleanly (append + done-set, run_tag cache-salting) — 0 corrupt lines, 0 dups, all cells full 5 reps.

2026-07-15 — B2 pilot: 2 ex × 5 cells (gpt-4.1 v2/v3 + flash v1/v2/v3) ≈ 200 calls, $0.08. Unparseable 0.0 across all 5 cells (flash v2/v3 clean too). Pilot cost cache-suppressed (gpt-4.1 cells pre-cached) — ignoring ×50; bottom-up est. from B1 rate ≈ $12–14 full. Cumulative would land ≈ $63. Launching N_EX=100.

2026-07-15 — B2 complete: 100 ex × 5 cells = 10,050 rows (2,010/cell, balanced), $11.66 (est. $12–14 bottom-up; runbook $16–21). Cumulative ≈ $62.3. Per-cell unparseable ≈0: gpt-4.1 both 0.0000; flash v1 0.0010, v3 0.0005, v2 0.0000 — terse-suppression hypothesis did NOT materialize. Hit OpenRouter key-limit 402 mid-run (max_tokens reserved at model ceiling vs key cap); raised key spend limit, resumed via append+done-set.

2026-07-15 — 5c Step 1 (model gap, B1): sonnet-4.5 0.478 vs gpt-4o-mini 0.370 → MODEL GAP = 0.108 (stronger wins, well above ~0.03 floor). Paired per-example diffs (mini−sonnet) saved to results/b1_paired_diffs.json: n=402, mean −0.108 (= −gap ✓), std 0.249 (~2.3× mean magnitude), median −0.082, range −1.0 (sonnet perfect / mini 0) to +0.78 (big mini upset). std/mean ≈ 2.3× — spread dwarfs the mean, which is why 5d power analysis matters. ~24% of diffs positive (mini wins) despite sonnet's overall edge.

2026-07-15 - Spot-read of mini>sonnet upsets: (1) insulin ex — genuine judge mis-grade, a −5 penalty on content that Sonnet clearly included; individual-example judge noise. (2) prior-auth ex — benchmark blind spot: principled refusal scored as total failure, no criterion for refusal/deferral, and mini's mild fabrication unpenalized. Refusal rate for Sonnect checked: ~5 clear refusals (score mean 0.10), excluding them shifts sonnet mean 0.478→0.483 (~0.005 of 0.108 gap) — NOT a gap driver. Conclusion: 0.108 gap is mostly real rubric-coverage quality diff; per-example scores carry judge noise; refusal effect real but rare.

2026-07-15 — 5c Steps 2-3 (spreads vs MODEL GAP 0.108): grid complete, no NaN (B1 v1 stitched OK). Spreads [sonnet / mini / avg]: reps 0.034/0.033/0.034 (31% of gap), judge 0.049/0.106/0.077 (71%), variant 0.071/0.124/0.098 (91%). Ordering reps < judge < variant as predicted. FINDING: nuisance spreads comparable to the gap, not <<. gpt-4o-mini variant spread 0.125 EXCEEDS the gap and judge spread 0.106 ≈ gap — for the weak model, judge/prompt choice moves the score more than the model difference itself. Weak model far more config-sensitive than strong (variant 0.125 vs 0.071). Driver: v3_clinical_persona lowest everywhere; gpt-4.1×v3 harshest cell (mini 0.348, outlier); gpt-4.1 judge harsher than flash.

2026-07-15 — 5c Step 5 (ANOVA, per response model). SONNET: judge p=0.123, variant p=0.201 — neither significant; strong model robust to config. MINI: judge p=0.0007 (sum_sq 1.19), variant p=0.032 (sum_sq 0.71) — BOTH significant; weak model's score moves with config. Judge is the larger MAIN effect for mini (sum_sq/marginal), though single-slice spread ranked variant higher (gpt-4.1×v3=0.348 dip inflated the gpt-4.1-row variant spread). Interaction NS both models (sonnet p=0.80, mini p=0.33) → additive, no rogue cell (resolves the outlier-cell caveat). Residual ~60 vs factors ~1.2/0.7: judge+variant explain only ~2-3% of total score variance; example difficulty dominates. Eval config significantly perturbs the WEAK model, not the strong one.

2026-07-15 — 5c Step 5 (block on prompt_id): example difficulty = 86% (sonnet) / 78% (mini) of total score variance — dominates. Blocking on example flips judge+variant to significant for BOTH models (p≈0); Step 5's "sonnet not significant" was a power artifact of not blocking, not absence of effect. Effect sizes unchanged; robust finding is MAGNITUDE: mini judge effect ~5× sonnet's, variant ~2×. Leading nuisance factor differs: sonnet variant>judge, mini judge>variant. Interaction still NS.

2026-07-15 — 5c Step 6 (clustered vs naive bootstrap, criterion level; 402 clusters, ~24.5 rows each). PAIRED model-difference estimand: ratio 0.83× — naive OVERstates (clustered 0.0321 < naive 0.0387). Registered prediction (naive understates 1.5-3×) FALSIFIED for this estimand. WITHIN-MODEL means: ratio 1.22× (sonnet), 1.32× (mini) — naive understates, correct direction, but below predicted 1.5-3×. Mechanism: clustering preserves model-to-model pairing → tightens the difference; for single-model means only criterion-clustering operates → inflates. Lesson: clustering correction sign is estimand-dependent. (Track A control 1.03×: tiny clusters, neither effect strong.)

2026-07-15 — 5d power analysis (power.py, fig_power.png). Sim vs formula sanity check PASS: sim power at formula MDE = 0.810/0.804/0.801/0.802 for n=100/200/400/800 (n=100 slightly high = normal-approx + skew at small n, converges to 0.80). MDE(n): ~0.070 @100, ~0.049 @200, ~0.035 @400, ~0.025 @800. Model gap 0.108 detectable well below n=400. The smallest detectable effects (0.035–0.070) are of the same order as the variability introduced by judge and prompt choice (0.078 and 0.098). While large model differences are easy to detect and robust to evaluation choices, small leaderboard-level differences may be sensitive to the choice of judge or prompt sample, making rankings less stable across evaluation configurations

2026-07-27 - Deep dive into top 50 cases where LLM judges disagreed with physician graders the most. Annotated failure taxonomy and found that 50% of cases were label noise (where physician graders did not correctly grade the model output based on criteria provided)