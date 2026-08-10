
'use client';

import { useState } from 'react';

export default function Home() {
  const [form, setForm] = useState({ name: '', email: '', phone: '', agency: '', interest: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    if (res.ok) setSubmitted(true);
  };

  return (
    <div className='flex flex-col flex-1 bg-black'>
      <header className='w-full border-b border-white/10 bg-black/50 backdrop-blur-md fixed top-0 z-50'>
        <div className='max-w-7xl mx-auto px-6 py-4 flex items-center justify-between'>
          <div className='text-2xl font-bold bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent'>
            PropertyVala
          </div>
          <nav className='hidden md:flex gap-8 text-sm text-zinc-400'>
            <a href='#how-it-works' className='hover:text-white transition'>How It Works</a>
            <a href='#pricing' className='hover:text-white transition'>Pricing</a>
            <a href='#leads' className='hover:text-white transition'>Lead Quality</a>
            <a href='#contact' className='hover:text-white transition'>Contact</a>
          </nav>
          <a href='#contact' className='px-5 py-2 rounded-full bg-white text-black text-sm font-medium hover:bg-zinc-200 transition'>
            Get Leads
          </a>
        </div>
      </header>

      <main>
        {/* Hero Section with Image */}
        <section className='relative min-h-screen flex items-center justify-center overflow-hidden pt-20'>
          <div className='absolute inset-0 bg-gradient-to-b from-indigo-900/20 via-black to-black' />


              backgroundImage: `radial-gradient(circle at 25% 25%, rgba(99,102,241,0.15) 0%, transparent 50%), radial-gradient(circle at 75% 75%, rgba(139,92,246,0.15) 0%, transparent 50%)`


                </p>

                <div className='flex flex-col sm:flex-row gap-4 justify-start'>
                  <a href='#contact' className='px-8 py-4 rounded-full bg-white text-black font-medium hover:bg-zinc-200 transition text-lg'>
                    Start Free Trial
                  </a>
                  <a href='#how-it-works' className='px-8 py-4 rounded-full border border-white/20 text-white hover:bg-white/5 transition text-lg'>
                    See How It Works
                  </a>
                </div>

                <div className='mt-10 grid grid-cols-3 gap-6 max-w-xl mx-auto'>
                  <div className='text-center'>
                    <div className='text-3xl font-bold text-white'>2,400+</div>
                    <div className='text-sm text-zinc-500 mt-1'>Verified Leads</div>
                  </div>
                  <div className='text-center'>
                    <div className='text-3xl font-bold text-white'>92%</div>
                    <div className='text-sm text-zinc-500 mt-1'>Contact Accuracy</div>
                  </div>
                  <div className='text-center'>
                    <div className='text-3xl font-bold text-white'>18%</div>
                    <div className='text-sm text-zinc-500 mt-1'>Avg. Conversion</div>
                  </div>
                </div>
              </div>

              {/* Image Content */}
              <div className='hidden lg:block flex-1 max-w-[400px] relative'>
                <div className='absolute inset-0 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-500 opacity-20 blur-3xl' />
                <img src='/images/screenshot-overview.png' 
                     alt='PropertyVala dashboard overview' 
                     className='rounded-2xl border border-white/5 drop-shadow-lg 
                                hover:scale-105 transition-transform duration-500'
                    />
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section with Images */}
        <section id='how-it-works' className='py-24 bg-black'>
          <div className='max-w-7xl mx-auto px-6'>
            <h2 className='text-4xl md:text-5xl font-bold text-center mb-16'>
              How <span className='bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent'>PropertyVala</span> works
            </h2>
            <p className='text-center text-zinc-400 mb-12 max-w-2xl mx-auto'>
              Our proven three-step process turns buyer intent into closed deals.
            </p>
            <div className='grid md:grid-cols-3 gap-8'>
              {[ 
                { 
                  title: 'We source intent signals', 
                  desc: 'Property portals, social ads, search behavior, form fills — aggregated into verified buyer profiles.',
                  imgSrc: '/images/screenshot-scoring.png',
                  imgAlt: 'Lead scoring interface showing intent signals'
                },
                { 
                  title: 'AI scores every lead 0-100', 
                  desc: 'Six-factor scoring: timeline, budget, contact quality, digital presence, property specificity, delivery source.',
                  imgSrc: '/images/screenshot-analytics.png',
                  imgAlt: 'Analytics dashboard showing lead scores'
                },
                { 
                  title: 'You close more deals', 
                  desc: 'Hot leads delivered to your dashboard. Swipe right to engage, track follow-ups, measure ROI.',
                  imgSrc: '/images/screenshot-crm.png',
                  imgAlt: 'CRM interface showing lead management'
                },
              ].map((item) => (
                <div key={item.title} className='group relative'>
                  <div className='aspect-w-16 aspect-h-9 mb-6 rounded-2xl overflow-hidden border border-white/5'>
                    <img 
                      src={item.imgSrc} 
                      alt={item.imgAlt} 
                      className='w-full h-full object-cover transition-transform duration-500 group-hover:scale-105'
                    />
                    <div className='absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300'>
                      <div className='absolute bottom-4 left-4 right-4 text-white text-sm font-medium'>
                        {item.title}
                      </div>
                    </div>
                  </div>
                  <div className='space-y-4'>
                    <h3 className='text-xl font-semibold text-white'>{item.title}</h3>
                    <p className='text-zinc-400 leading-relaxed'>{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section id='pricing' className='py-24 bg-surface'>
          <div className='max-w-7xl mx-auto px-6'>
            <h2 className='text-4xl md:text-5xl font-bold text-center mb-4'>Simple, transparent pricing</h2>
            <p className='text-center text-zinc-400 mb-16'>Pay for results, not lists.</p>
            <div className='grid md:grid-cols-3 gap-6 max-w-5xl mx-auto'>
              {[
                { tier: 'Starter', price: '5,000/mo', includes: '50 leads, basic CRM, WhatsApp support' },
                { tier: 'Growth', price: '15,000/mo', includes: '200 leads, analytics, API access, priority support' },
                { tier: 'Enterprise', price: 'Custom', includes: 'Unlimited leads, dedicated manager, SLA, white-label' },
              ].map((plan) => (
                <div key={plan.tier} className='group p-8 rounded-2xl bg-black border border-white/5 hover:border-indigo-500/30 transition flex flex-col'>
                  <div className='text-sm text-indigo-400 font-medium mb-2 flex items-center gap-2'>
                    <span className='w-3 h-3 bg-indigo-400 rounded' />
                    <span>{plan.tier}</span>
                  </div>
                  <div className='text-4xl font-bold mb-4 flex items-center baseline'>
                    <span>&#8377;</span>
                    <span className='text-5xl'>{plan.price}</span>
                  </div>
                  <div className='text-zinc-500 text-sm mb-6 flex-1'>{plan.includes}</div>
                  <a href='#contact' className='mt-auto w-full py-3 rounded-full bg-white text-black text-center font-medium hover:bg-zinc-200 transition'>
                    Get Started
                  </a>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section id='contact' className='py-24 bg-black'>
          <div className='max-w-3xl mx-auto px-6'>
            <h2 className='text-4xl md:text-5xl font-bold text-center mb-4'>Start your free trial</h2>
            <p className='text-center text-zinc-400 mb-10'>10 leads free. No credit card required.</p>
            {submitted ? (
              <div className='p-8 rounded-2xl bg-green-500/10 border border-green-500/30 text-center text-green-400'>
                <div className='text-2xl font-semibold mb-2'>We received your request</div>
                <p>Our team will reach out within 24 hours with your first 10 leads.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className='p-8 rounded-2xl bg-surface border border-white/5 space-y-5'>
                <div className='grid md:grid-cols-2 gap-5'>
                  <input required placeholder='Full name' value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} 
                    className='w-full px-4 py-3 rounded-xl bg-black border border-white/10 text-white placeholder-zinc-500 focus:border-indigo-500 focus:outline-none' />
                  <input required type='email' placeholder='Work email' value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} 
                    className='w-full px-4 py-3 rounded-xl bg-black border border-white/10 text-white placeholder-zinc-500 focus:border-indigo-500 focus:outline-none' />
                  <input required type='tel' placeholder='Phone number' value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} 
                    className='w-full px-4 py-3 rounded-xl bg-black border border-white/10 text-white placeholder-zinc-500 focus:border-indigo-500 focus:outline-none' />
                  <input required placeholder='Agency / Brokerage name' value={form.agency} onChange={(e) => setForm({ ...form, agency: e.target.value })} 
                    className='w-full px-4 py-3 rounded-xl bg-black border border-white/10 text-white placeholder-zinc-500 focus:border-indigo-500 focus:outline-none' />
                </div>
                <textarea rows={3} placeholder='What properties are you buying/selling? (land, apartments, budget, locations)' value={form.interest} onChange={(e) => setForm({ ...form, interest: e.target.value })} 
                  className='w-full px-4 py-3 rounded-xl bg-black border border-white/10 text-white placeholder-zinc-500 focus:border-indigo-500 focus:outline-none' />
                <button type='submit' className='w-full py-4 rounded-full bg-white text-black font-semibold text-lg hover:bg-zinc-200 transition'>
                  Claim My 10 Free Leads
                </button>
                <p className='text-xs text-zinc-500 text-center'>By submitting you agree to our Terms and Privacy Policy.</p>
              </form>
            )}
          </div>
        </section>
      </main>

      <footer className='border-t border-white/10 py-8 bg-black'>
        <div className='max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4'>
          <div className='text-zinc-500 text-sm'>PropertyVala.com — AI-powered real estate lead generation.</div>
          <div className='flex gap-6 text-zinc-500 text-sm'>
            <a href='#' className='hover:text-white transition'>Terms</a>
            <a href='#' className='hover:text-white transition'>Privacy</a>
            <a href='#' className='hover:text-white transition'>Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

